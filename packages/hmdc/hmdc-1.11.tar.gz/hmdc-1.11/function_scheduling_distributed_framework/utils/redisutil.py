import traceback
import redis
import time
import threading

from redis.exceptions import LockError 


class XRedis:
    def __init__(self, host, password, port, db=0):
        self.host = host
        self.password = password
        self.port = port
        self.db = db
        self.locker = threading.Lock()
        self.connection_lost = True
        
        self._make_conn()
        
    def _background_heartbeat(self):
        print('开始心跳')
        if hasattr(self, 'heartbeat_thread'):
            if self.heartbeat_thread.isAlive():
                self.heartbeat_thread.stop()
            del self.heartbeat_thread
            
        self.heartbeat_thread = threading.Thread(target=self._ping, args=())
        self.heartbeat_thread.daemon = True
        self.heartbeat_thread.start()
        # self._ping()
        
    def _ping(self):
        while not self.connection_lost:
            if self.set('ping', 'ok', expired=30):
                print('pinged')
            else:
                self.connection_lost = True
                print('连接丢失')
                
            time.sleep(30)
            
    def __release_conn(self):
        if hasattr(self, 'conn'):
            print('释放连接')
            del self.conn
    
    def _make_conn(self):
        try:
            self.__release_conn()
            print('创建新连接')
            pool = redis.ConnectionPool(
                host=self.host, password=self.password, port=self.port, db=self.db, decode_responses=True, max_connections=4, socket_timeout=300, socket_connect_timeout=30, socket_keepalive=True)
            self.conn = redis.StrictRedis(connection_pool=pool)
            # self.conn = redis.StrictRedis(host=self.host, port=self.port, db=self.db, password=self.password, decode_responses=True, socket_connect_timeout=1, socket_timeout=1)
            if self.conn.ping():
                self.connection_lost = False
                self._background_heartbeat()
                return True
            else:
                print('连接失败, 网络错误')
                self.connection_lost = True
                return False
        except Exception as e:
            print('连接失败, 网络错误')
            self.connection_lost = True
            return False
            
    def __get_connection(self, pipeline, transaction):
        if not self.connection_lost and hasattr(self, 'conn'):
            if pipeline:
                return self.conn.pipeline(transaction=transaction)
            else:
                return self.conn
        return None

    def _get_connection(self, pipeline=False, transaction=False):
        conn = self.__get_connection(pipeline, transaction)
        
        if conn is None:
            with self.locker:
                conn = self.__get_connection(pipeline, transaction)
                if conn is None:
                    while not self._make_conn():
                        time.sleep(0.1)
                    
                    conn = self.conn
           
        return conn

    def lock(self, lock_id, ttl=60, tries=0):
        try:
            conn = self._get_connection()
            print('获取锁 -> {}'.format(lock_id))
            return conn.lock('lock_' + lock_id, blocking_timeout=1, timeout=ttl)
        except LockError as error:
            print(str(error))
            return None
        except Exception as e:
            if tries < 3:
                time.sleep(0.1)
                return self.lock(lock_id, ttl, tries + 1)
            else:
                traceback.print_exc()

    def lock_set(self, key, val, expired=None):
        with self.lock(key):
            self.set(key, val, expired=expired)

    def set(self, key, val, expired=None, tries=0):
        conn = self._get_connection()
        try:
            conn.set(key, val)
            if expired is not None:
                conn.expire(key, expired)
            return True
        except Exception as e:
            if tries < 3:
                time.sleep(0.1)
                self.set(key, val, expired, tries + 1)
            else:
                traceback.print_exc()
        return False

    def set_expire_time(self, key, expired):
        conn = self._get_connection()
        conn.expire(key, expired)

    def lock_get(self, key):
        with self.lock(key):
            return self.get(key)

    def get(self, key):
        conn = self._get_connection()
        return conn.get(key)

    def delkey(self, key):
        conn = self._get_connection()
        return conn.delete(key)

    def batch_set(self, map: dict):
        conn = self._get_connection()
        conn.mset(map)

    def batch_get(self, keys):
        conn = self._get_connection()
        return conn.mget(keys)

    def list_create(self, key):
        conn = self._get_connection()
        conn.lrem

    def list_append(self, key, value, create_if_not_exists=True):
        conn = self._get_connection()
        if create_if_not_exists:
            conn.rpush(key, value)
        else:
            conn.rpushx(key, value)

    def list_prepend(self, key, values, create_if_not_exists=True):
        conn = self._get_connection()
        if create_if_not_exists:
            conn.lpush(key, values)
        else:
            conn.lpushx(key, values)

    def list_len(self, key):
        conn = self._get_connection()
        return conn.llen(key)

    def list_range(self, key, start, end):
        conn = self._get_connection()
        return conn.lrange(key, start, end)

    def list_index(self, key, index):
        conn = self._get_connection()
        return conn.lindex(key, index)

    def list_get(self, key):
        conn = self._get_connection()
        return conn.lpop(key)

    def hash_incre(self, hashname, key, amount=1):
        conn = self._get_connection()
        return conn.hincrby(hashname, key, amount)

    def hash_decre(self, hashname, key, amount=1):
        conn = self._get_connection()
        return conn.hincrby(hashname, key, -amount)

    def hash_set(self, hashname, key, val):
        conn = self._get_connection()
        conn.hset(hashname, key, val)

    def hash_get(self, hashname, key):
        conn = self._get_connection()
        return conn.hget(hashname, key)

    def hash_keys(self, hashname):
        conn = self._get_connection()
        return conn.hkeys(hashname)

    def hash_items(self, hashname):
        conn = self._get_connection()
        return conn.hgetall(hashname)

    def hash_contains(self, hashname, key):
        conn = self._get_connection()
        return conn.hexists(hashname, key)

    def hash_del(self, hashname, key):
        conn = self._get_connection()
        return conn.hdel(hashname, key)

    def incr(self, key):
        conn = self._get_connection()
        return conn.incr(key, 1)
    
    def blpop(self, key):
        conn = self._get_connection()
        return conn.blpop(key)
    
    def blpush(self, key, val):
        conn = self._get_connection()
        return conn.rpush(key, val)
    
    def lcount(self, key):
        conn = self._get_connection()
        return conn.llen(key)
    
    def get_pubsub(self):
        conn = self._get_connection()
        return conn.pubsub()
    
    def get_hmget(self, hashname, keys):
        conn = self._get_connection()
        return conn.hmget(hashname, keys)
    
    def zadd(self, z_name, member, val):
        conn = self._get_connection()
        return conn.zadd(z_name, {
            member: val
        })
        
    def zrange(self, z_name, score_min, score_max):
        conn = self._get_connection()
        return conn.zrangebyscore(z_name, score_min, score_max)
    
    def zcount(self, z_name, score_min, score_max):
        conn = self._get_connection()
        return conn.zcount(z_name, score_min, score_max)