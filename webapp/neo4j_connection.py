from neo4j import GraphDatabase


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
        
    # TODO removes if necessary
    def get_books(self, uid, similarity_score = 0.6):
        with self.driver as driver:

            # TODO make another class or functions that returns the paramaters
            parameters = {
                "uid": uid,
                "score": similarity_score
            }
            query = """
                        MATCH (targetUser:User {userId: toInteger($uid)})-[similar:SIMILAR]->(similarUser:User)-[rated:RATED]->(b:Book)
                        WHERE similar.score >= toInteger($score)
                        WITH DISTINCT {title: b.title, author: b.author, publisher: b.publisher, year: b.year, isbn: b.isbn} as similarBooks
                        UNWIND similarBooks as books
                        RETURN books ORDER BY books
                    """

            records, summary, keys = driver.execute_query(
                query,
                database_="neo4j",
                parameters_=parameters,
            )

            # reorganize the result as a list of list
            result = []
            for record in records:  
                result.append(record['books'])

            # Summary information  
            print("The query returned {records_count} records in {time} ms.".format(
                records_count=len(records),
                time=summary.result_available_after
            ))
            return result
    

if __name__ == "__main__":
    # conn = Neo4jConnection(DB_URL, DB_USERNAME, DB_PASSWORD)
    # conn.get_books()
    # conn.close()
    pass