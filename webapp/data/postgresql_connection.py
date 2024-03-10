import psycopg2
from webapp.db_config import config


class PGConnection:
    def __init__(self):
        self.conn = None
        try:
            params = config(
                filename="db_init/pg.ini",
                section="postgresql",
            )
            
            self.conn = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close(self):
        if self.conn is not None:
            self.conn.close()

    def get_books(self, count,title="", uid=1, limit=1000):
        with self.conn as conn:
            with conn.cursor() as cur:
                if title:
                    if count > 1000:

                        cur.execute(
                            "SELECT * FROM book WHERE LOWER(title) LIKE LOWER(%s) LIMIT %s",
                            ("%" + title + "%", limit),
                        )
                    else:
                        cur.execute(
                            "SELECT * FROM book WHERE LOWER(title) LIKE LOWER(%s) ",
                            ("%" + title + "%",)
                        )

                else:
                    if count > 1000:

                        cur.execute(
                            "SELECT * FROM generate_recommendations(%s) LIMIT %s",
                            (uid, limit,)
                        )
                    else:
                        cur.execute(
                            "SELECT * FROM generate_recommendations(%s)",
                            (uid,)
                        )
                
                records = cur.fetchall()
                result = []
                for record in records:
                    result.append(
                        {
                            "isbn": record[0],
                            "title": record[1],
                            "author": record[2],
                            "year": record[3],
                            "publisher": record[4],
                        }
                    )

                return result

    def get_top_ten(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM top_ten()")

                while True:
                    records = cur.fetchall()
                    if not records:
                        break

                    result = []
                    for record in records:
                        result.append(
                            {
                                "country": record[0],
                                "title": record[1],
                            }
                        )

                    return result

    def insert_book(self, book):
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        "CALL insert_book(%s,%s,%s,%s,%s)",
                        (
                            book["isbn"],
                            book["title"],
                            book["author"],
                            book["year"],
                            book["publisher"],
                        ),
                    )
                    return True
                except psycopg2.Error as e:
                    return False


    def get_total_books(self,title='',uid=''):
        with self.conn as conn:
            total_count = 0
            with conn.cursor() as cur:
                if uid:
                    cur.execute(
                        "SELECT COUNT(*) FROM book WHERE LOWER(title) LIKE LOWER(%s) ",
                        ("%" + title + "%",),
                    )
                    
                    total_count = cur.fetchone()[0]

                else:
                    cur.execute(
                        "SELECT COUNT(*) FROM generate_recommendations(%s)",
                        (uid,)
                    )
                    
                    total_count = cur.fetchone()[0]

                return total_count