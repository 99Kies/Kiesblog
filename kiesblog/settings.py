import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 相当于该项目的根目录

print('__file__', __file__)
print('basedir', basedir)

class BaseConfig(object):
    # 将一些配置写入（SqlAlchemy，Mail...的配置)
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # FLASK_DEBUG=True
    KIESBLOG_POST_PER_PAGE = 10

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('KiesBlog Admin',MAIL_USERNAME)

    KIESBLOG_EMAIL = os.getenv('KIESBLOG_EMAIL')
    KIESBLOG_POST_PER_PAGE = 10
    KIESBLOG_MANAGE_POST_PER_PAGE = 15
    KIESBLOG_COMMENT_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # in-memory database

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))


config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig
}