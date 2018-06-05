import psycopg2
import traceback

class pgclient():
    '''This is a Postgresql Database Operation client. Quick start on Postgrsql Python connection.'''

    pg_connection = None

    pg_curosr = None

    def __init__(self, db = "", user = 'postgres', password = 'mercurypw', host = '127.0.0.1', port = '5432'):
        try:
            if not self.pg_connection:
                psycopg2.connect(db, user, password, host, port)

            if not self.pg_curosr:
                self.pg_curosr = self.pg_connection.cursor()
        except:
            traceback.print_exc()

    def execute(self, sql):
        self.pg_curosr.execute(sql)

    def execute

    def commit(self):
        self.pg_connection.commit()

    def rollback(self):
        self.pg_connection.rollback()
        self.pg_curosr.fetchone()

    def __del__(self):
        self.pg_curosr.close()
        self.pg_connection.close()
