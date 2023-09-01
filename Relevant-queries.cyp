// Get the user with the highest number of rated book --> 399 ms
MATCH (l:Location)<-[LIVES_IN]-(u:User)-[RATED]->() 
WITH u, count(*) as rating_count 
ORDER by rating_count DESC LIMIT 10 
RETURN u.userId as UID, l.country as userCountry, rating_count;
 
// Get the book with the highest number of read --> 394 ms
MATCH ()-[RATED]->(b:Book)
WITH b, count(*) as read_count
ORDER by read_count DESC LIMIT 10
return b.title as Title, read_count

// Get for every country the number of books that has been rated --> 557 ms 
MATCH (location:Location)<-[:LIVES_IN]-(user:User)-[r:RATED]->(book:Book)
WITH location.country AS country, COUNT(book) AS ratedBooksCount
RETURN country, ratedBooksCount
ORDER BY ratedBooksCount DESC
LIMIT 10;


// Get the user count for every country --> 121 ms
MATCH (l:Location)<-[LIVES_IN]-(u:User)
WITH l.country as country, count(u) as user_count
ORDER BY user_count DESC LIMIT 10
RETURN country, user_count


// Get for every country the books with the highest rating --> 2706 ms
MATCH (l:Location)<-[:LIVES_IN]-(u:User)
WITH l.country AS country, count(u) AS user_count
ORDER BY user_count DESC
LIMIT 10
MATCH (location:Location {country: country})<-[:LIVES_IN]-(user:User)-[r:RATED]->(book:Book)
WITH country, book.title AS title, r.rating AS rating
ORDER BY country, rating DESC
WITH country, COLLECT({title: title})[0..10] AS topRatedBooks
RETURN country, topRatedBooks;
