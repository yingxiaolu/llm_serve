from flask import g
import pymysql


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host='rm-wz9fveh412f250974oo.mysql.rds.aliyuncs.com',
            port=3306,
            user='lixuan',
            password='ieshei8E1Eishoom8')
    return g.db
    #if 'db' not in g:
    #    g.db = pymysql.connect(
    #        host='106.14.171.72',
    #        port=6009,
    #        user='product',
    #        password='pl,okm098')
    #return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


if __name__ == "__main__":
    print("hello")
