// Get users that have read at least 5 common books
MATCH (u1:User)-[r1:RATED]->(b:Book)<-[r2:RATED]-(u2:User)
WHERE u1.userId <> u2.userId
WITH count(distinct b.isbn) as common_read, u1, u2
WHERE common_read >= 5 
RETURN u1.userId as u1 ,u2.userId as u2, common_read
LIMIT 100

// Get the user with the highest number of rated book --> 399 ms
MATCH (l:Location)<-[LIVES_IN]-(u:User)-[RATED]->() 
WITH u, count(*) as rating_count,l 
ORDER by rating_count DESC LIMIT 10 
RETURN u.userId as UID, l.country as userCountry, rating_count;
 
// Get the book with the highest number of read --> 394 ms
MATCH ()-[r:RATED]->(b:Book)
WITH b, count(*) as read_count
ORDER by read_count DESC LIMIT 10
RETURN b.title as Title, read_count

// Get for every country the number of books that have been rated --> 557 ms 
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


// Get for every country the books with the highest rating --> 1500 ms
MATCH (l:Location)<-[:LIVES_IN]-(u:User)
WITH l.country AS country, count(u) AS user_count
ORDER BY user_count DESC LIMIT 10
MATCH  (location:Location {country: country})<-[:LIVES_IN]-(user)-[r:RATED]->(book:Book)
WITH location.country AS country, book, COUNT(r) AS ratingCount
ORDER BY country, ratingCount DESC
WITH country, COLLECT({book: book, ratingCount: ratingCount})[0] AS topBook
RETURN country, topBook.book.title AS TopBookTitle


// Given a user it provides suggested books considering the rating to the same book
MATCH (targetUser:User {userId: 249688})-[r1:RATED]->(targetBook:Book)<-[r2:RATED]-(similarUser:User)
WHERE similarUser <> targetUser AND abs(r1.rating - r2.rating) <= 3
WITH targetBook, targetUser, similarUser
MATCH (similarUser)-[:RATED]->(commonBook:Book)
WHERE commonBook <> targetBook
RETURN DISTINCT commonBook.isbn as isbn, commonBook.title as title
ORDER BY isbn DESC LIMIT 100

// Return a book node by passing a part of the title or the whole title
MATCH (book:Book)
WHERE toLower(book.title) =~ toLower('.*potter.*')  // Replace 'Potter' with your search term
RETURN book

// Get the average age of users who have rated books with a rating above 8
MATCH (u:User)-[r:RATED]->(b:Book)
WHERE r.rating >= 8 AND u.age is not null
RETURN AVG(toInteger(u.age)) 


// Find users who live in a specific country, have rated a book, 
// and are above a certain age
MATCH (l:Location)<-[r1:LIVES_IN]-(u:User)-[r2:RATED]->(b:Book)
WHERE l.country = 'italy' AND toInteger(u.age) >= 18.0
RETURN u.userId ORDER BY u.userId


// Compare how many books users under 30 years read,
MATCH (u:User)-[r:RATED]->(b:Book)
WHERE u.age <= 18 AND r.rating > 0
RETURN count(*)