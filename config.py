class BaseConfig(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CR_TEST_USERS = '/home/peter/Desktop/test_users.csv'


