

class Config:
    '''配置信息'''
    SECRET_KEY = 'secret key to protect from csrf'


class DevelopmentConfig(Config):
    DEBUG = True
    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@62.234.160.153:3306/yuan?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379


class ProductionConfig(Config):

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@62.234.160.153:3306/yuan?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
