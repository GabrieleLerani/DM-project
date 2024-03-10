from neo4j import GraphDatabase, exceptions
from webapp.db_config import config
from .cypher_queries import Query


class Neo4jConnection:
    def __init__(self):
        self.driver = None
        try:
            params = config(
                filename="db_init/neo4j.ini",
                section="neo4j",
            )

            self.driver = GraphDatabase.driver(
                params["uri"], auth=(params["username"], params["password"])
            )
            self.driver.verify_connectivity()
        except Exception as e:
            from flask import current_app

            current_app.logger.error("EXCEPTION: %s", e)

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def get_driver(self):
        if self.driver is not None:
            return self.driver
        return None

    def get_books(self, count, uid=1, title=""):
        with self.driver as driver:
            
            query, parameters = (
                Query.get_books_by_title(title)
                if title
                else Query.get_books_by_uid(uid)
            )

            records, summary, key = driver.execute_query(
                query,
                database_="neo4j",
                parameters_=parameters,
            )

            # reorganize the result as a list of lists
            result = []
            for record in records:
                result.append(record["books"])

            # Summary information
            print(
                "The query returned {records_count} records in {time} ms.".format(
                    records_count=len(records), time=summary.result_available_after
                )
            )
            return result

    def get_top_ten(self):
        with self.driver as driver:
            query = Query.get_books_top_ten()
            records, summary, key = driver.execute_query(
                query,
                database_="neo4j",
            )

            # reorganize the result as a list of lists
            result = []
            for record in records:
                result.append(record["result"])

            # Summary information
            print(
                "The query returned {records_count} records in {time} ms.".format(
                    records_count=len(records), time=summary.result_available_after
                )
            )
            return result

    def insert_book(self, book):
        with self.driver as driver:
            try:
                query = Query.get_insert_book()
                records, summary, key = driver.execute_query(
                    query, database_="neo4j", parameters_=book
                )

                print(
                    "The query returned {records_count} records in {time} ms.".format(
                        records_count=len(records), time=summary.result_available_after
                    )
                )
                return True
            except exceptions.Neo4jError as e:
                return False


    def get_total_books(self, title='', uid=''):
        with self.driver as driver:
            try:
                
                query, parameters = Query.get_total_book_by_uid(uid) if uid else Query.get_total_book_by_title(title)
                records, summary, key = driver.execute_query(query, database_="neo4j",parameters_=parameters)
                
                
                print("RECORDS: ",records[0][0])
                return records[0][0]

            except exceptions.Neo4jError as e:
                print(e)
                return False  