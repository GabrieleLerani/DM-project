from neo4j import GraphDatabase
from .queries import Query


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
        except Exception as e:
            print("Failed to create the driver", e)

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def get_driver(self):
        if self.driver is not None:
            return self.driver
        return None

    def get_books(self, uid=1, similarity_score=0.6, title=""):
        with self.driver as driver:
            query, parameters = (
                Query.get_books_by_title(title)
                if title
                else Query.get_books_by_uid(uid, similarity_score)
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
