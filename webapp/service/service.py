from webapp.data.neo4j_connection import Neo4jConnection
from webapp.data.postgresql_connection import PGConnection
from flask import g, Blueprint
from dotenv import load_dotenv
import os

main = Blueprint("main", __name__, template_folder="templates")

load_dotenv()
DB_TYPE = os.getenv("DB_TYPE")

class Service:
    def __init__(self) -> None:
        self.db_connection = None

    def get_db(self):
        if DB_TYPE == "PG":
            if not hasattr(g, "postgres"):
                g.postgres = PGConnection()

            self.db_connection=g.postgres
        else:
            if not hasattr(g, "neo4j"):
                g.neo4j = Neo4jConnection()
            self.db_connection=g.neo4j

    def get_top_ten(self):
        if not self.db_connection:
            self.get_db()
            

        return self.db_connection.get_top_ten()

    def insert_book(self, book):
        if not self.db_connection:
            self.get_db()
            
        
        return self.db_connection.insert_book(book)
        


    def get_books_by_user(self, q):
        if not self.db_connection:
            self.get_db()
            
        count = self.__get_books_count(uid=q)
        return self.db_connection.get_books(uid=q, count=count)
        

    def get_books_by_title(self, q):
        if not self.db_connection:
            self.get_db()
        
        count = self.__get_books_count(title=q)

        return self.db_connection.get_books(title=q, count=count)

    def __get_books_count(self, title='', uid=''):
        if not self.db_connection:
            self.get_db()

        if uid:
            
            return self.db_connection.get_total_books(uid=uid)
        else:
            return self.db_connection.get_total_books(title=title)


    @main.teardown_request
    def teardown_db(self,exception):
        db = g.pop("postgres", None)

        if db is not None:
            db.close()


