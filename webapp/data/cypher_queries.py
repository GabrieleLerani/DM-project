class Query(object):
    def __init__(self) -> None:
        pass

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Query, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_books_by_uid(uid, score=0.7):
        return """
                    MATCH  (bTarget:Book)<-[ratedTarget:RATED]-(targetUser:User {userId: toInteger($uid)})-[similar:SIMILAR]->(similarUser:User)-[rated:RATED]->(b:Book)
                    WHERE similar.score >= toInteger($score) AND b.isbn <> bTarget.isbn
                    WITH DISTINCT {title: b.title, author: b.author, publisher: b.publisher, year: b.year, isbn: b.isbn} as similarBooks
                    UNWIND similarBooks as books
                    RETURN books ORDER BY books.title
                """, {
            "uid": uid,
            "score": score,
        }

    @staticmethod
    def get_books_by_title(title):
        return """
                    MATCH (b:Book)
                    WHERE toLower(b.title) =~ toLower($title)  
                    RETURN {title: b.title, author: b.author, publisher: b.publisher, year: b.year, isbn: b.isbn} as books
                    LIMIT 1000 
                """, {
            "title": ".*" + title + ".*"
        }

    @staticmethod
    def get_books_top_ten():
        return """
                    MATCH (l:Location)<-[:LIVES_IN]-(u:User)
                    WITH l.country AS country, count(u) AS user_count
                    ORDER BY user_count DESC
                    LIMIT 10
                    MATCH (location:Location {country: country})<-[:LIVES_IN]-(user:User)-[r:RATED]->(book:Book)
                    WHERE r.rating > 8
                    WITH country, book.title AS title, r.rating AS rating
                    WITH country, COLLECT({title: title})[0..1] AS topRatedBooks
                    RETURN {country: country, title: topRatedBooks[0]["title"]} AS result                
                """

    @staticmethod
    def get_insert_book():
        return """
                CREATE (b:Book)
                SET b.isbn = $isbn, b.author = $author, b.title = $title, b.publisher = $publisher , b.year = $year 
                """


    @staticmethod
    def get_total_book_by_title(title):
        return """
                    MATCH (b:Book)
                    WHERE toLower(b.title) =~ toLower($title)  
                    RETURN COUNT(*)
                """, {
            "title": ".*" + title + ".*"
        }
    
    @staticmethod
    def get_total_book_by_uid(uid, score=0.6):
        return """
                    MATCH  (bTarget:Book)<-[ratedTarget:RATED]-(targetUser:User {userId: toInteger($uid)})-[similar:SIMILAR]->(similarUser:User)-[rated:RATED]->(b:Book)
                    WHERE similar.score >= toInteger($score) AND b.isbn <> bTarget.isbn
                    WITH COLLECT(DISTINCT b.isbn) as similarBooks
                    UNWIND similarBooks as books
                    RETURN count(*)
                """, {
            "uid": uid,
            "score": score,
        }