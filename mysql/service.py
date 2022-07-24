import pymysql

def getMySQLClient(host, port, username, password, db):
    con = pymysql.connect(host=host, 
                          port=port,
                          user=username, 
                          password=password, 
                          db=db, 
                          charset='utf8'
                        )
    return con

class StoreException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors

class AbstractRepository:
    def __init__(self, host, port, username, password, db):
        try:
            self.conn = getMySQLClient(host, int(port), username, password, db)
        except Exception as e:
            raise StoreException(*e.args, **e.kwargs)
        self._complete = False

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        # can test for type and handle different situations
        self.close()

    def complete(self):
        self._complete = True

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise StoreException(*e.args)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise StoreException(*e.args)