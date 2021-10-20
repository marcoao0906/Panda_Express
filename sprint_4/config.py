class dev():
    DEBUG = True 
    SECRET_KEY = "2k311ko"
    DATABASE = {
        'name': 'db.sqlite3',
        'engine':'peewee.SqliteDatabase'
    }

class prod():
    DEBUG = False 
    SECRET_KEY = "12345"
    DATABASE = {
        'name': 'pandaexpress.sqlite3',
        'engine':'peewee.MysqlDatabase',
        'host':'url.donde.esta.mi.db.com',
        'user':'jessica',
        'passwd':'1111111'

    }