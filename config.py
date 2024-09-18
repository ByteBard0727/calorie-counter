# for CSRF protection
class Config:
    SECRET_KEY = 'mew'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#config SQLAlchemy for the dev envi
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:<YourPassword>@localhost/calorie-counter?driver=ODBC+Driver+17+for+SQL+Server'

#config SQLAlchemy for the prod envi
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:<YourPassword>@localhost/calorie-counter?driver=ODBC+Driver+17+for+SQL+Server'
