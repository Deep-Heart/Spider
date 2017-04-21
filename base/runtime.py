DEBUG = True
LOCAL_TEST_SERVER = "192.168.198.242"


class DbConfig(object):

    @staticmethod
    def get_db_info():
        redis_host, redis_port = DbConfig.get_redis_info()
        mongo_server, mongo_port = DbConfig.get_mongo_info()

        return mongo_server, mongo_port, redis_host, redis_port

    @staticmethod
    def get_redis_info():
        redis_host = 'localhost'
        redis_port = 6379

        return redis_host, redis_port

    @staticmethod
    def get_mongo_info():
        if DEBUG is False:
            mongo_server = ["10.19.136.122", "10.19.63.98", "10.19.87.123"]
            mongo_port = 5010
        else:
            mongo_server = LOCAL_TEST_SERVER
            mongo_port = 27017

        return mongo_server, mongo_port
