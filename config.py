class dev():
    DEBUG = True 
    SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
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