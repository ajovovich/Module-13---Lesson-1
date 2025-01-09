class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Tuckerstriker12@127.0.0.1:3306/factory_management_db'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True

class TestingConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Tuckerstriker12@127.0.0.1:3306/factory_management_db'
    DEBUG = True