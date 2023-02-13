class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///kanban_db.sqlite3'
    DEBUG = True
    SECRET_KEY = 'secret-key-for-session'