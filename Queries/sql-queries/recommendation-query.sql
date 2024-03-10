-- User-based collaborative filtering recommendation for a specific user (user_id)
WITH UserRatings AS (
    SELECT r.isbn, CAST(r.rating AS numeric) AS rating_numeric
    FROM rating r
    WHERE r.uid = '249688'
),
SimilarUsers AS (
    SELECT r.uid AS similar_userid, COUNT(*) AS num_common_ratings
    FROM rating r
    JOIN UserRatings ur ON r.isbn = ur.isbn
    WHERE r.uid <> '249688'
    GROUP BY r.uid
    HAVING COUNT(*) >= 3
),
RecommendedBooks AS (
    SELECT b.isbn, b.title
    FROM rating r
    JOIN SimilarUsers su ON r.uid = su.similar_userid
    JOIN book b ON r.isbn = b.isbn
    LEFT JOIN UserRatings ur ON r.isbn = ur.isbn
    WHERE ur.isbn IS NULL  -- Exclude books already rated by the user
    GROUP BY b.isbn, b.title
    ORDER BY AVG(CAST(r.rating AS numeric)) DESC
    LIMIT 10  -- Number of recommendations to generate
)
SELECT b.isbn, b.title, b.author, b.publisher, b.year FROM RecommendedBooks rb
JOIN book b ON rb.isbn = b.isbn
ORDER BY b.isbn DESC;

-- Get users that have read at least 5 common books
SELECT u1.userid AS user1, u2.userid AS user2, COUNT(DISTINCT r1.isbn) as common_read
FROM user_data u1 
INNER JOIN user_data u2 ON u1.userid < u2.userid
INNER JOIN rating r1 ON u1.userid = r1.uid
INNER JOIN rating r2 ON u2.userid = r2.uid
WHERE r1.isbn = r2.isbn
GROUP BY u1.userid, u2.userid
HAVING COUNT(DISTINCT r1.isbn) >= 5 LIMIT 100;


-- Get users that have read at least 5 common books for a target user
WITH target_user AS (
    SELECT userid
    FROM user_data
    WHERE userid = '100004' -- Replace with the desired user's ID
)
SELECT u1.userid AS user1, u2.userid AS user2
FROM user_data u1
INNER JOIN user_data u2 ON u1.userid < u2.userid
INNER JOIN rating r1 ON u1.userid = r1.uid
INNER JOIN rating r2 ON u2.userid = r2.uid
INNER JOIN target_user t ON u1.userid = t.userid
WHERE r1.isbn = r2.isbn
GROUP BY u1.userid, u2.userid
HAVING COUNT(DISTINCT r1.isbn) >= 5;

-- Get the book with the highest number of read 
WITH ratedBooks AS (
	SELECT r.isbn, count(r.isbn) as readCount
	FROM rating r
    WHERE CAST(r.rating AS numeric) >= 8.0 
	LEFT JOIN book b ON r.isbn = b.isbn
	GROUP BY r.isbn
	ORDER BY readCount DESC
	LIMIT 10
)
SELECT book.title, readCount
FROM book JOIN ratedBooks ON ratedBooks.isbn = book.isbn;



-- Get for every country the books with the highest rating
WITH country_count AS (
	-- Get the user count for every country
	SELECT country, count(*) as user_count
	FROM user_data
	WHERE country is not NULL and province is not NULL
	GROUP BY country
	ORDER BY user_count DESC
	LIMIT 10
),
ranked_books AS (
    SELECT
        ud.country,
        b.title AS book_title,
        COUNT(r.uid) AS rating_count,
        RANK() OVER (PARTITION BY ud.country ORDER BY COUNT(r.uid) DESC) AS rating_rank
    FROM
        user_data ud
	
    INNER JOIN
        rating r ON ud.userid = r.uid
    INNER JOIN
        book b ON r.isbn = b.isbn
    GROUP BY
        ud.country, b.title
)
SELECT rb.country,rb.book_title
FROM ranked_books rb
WHERE rb.rating_rank = 1
	and rb.country in (select country from country_count);


-- Get book by title
SELECT * FROM book WHERE LOWER(title) LIKE LOWER('%potter%')


-- Get the average age of users who have rated books with a rating above 8
SELECT ROUND(AVG(CAST(ur.age as NUMERIC)),2) as avg_age
FROM rating r
JOIN user_data ur ON ur.userid = r.uid
WHERE r.rating >= '8'


-- Find users who live in a specific country, have rated a book, 
-- and are above a certain age
SELECT ur.userid
FROM rating r
JOIN user_data ur ON ur.userid = r.uid
WHERE ur.country = 'italy' AND
	ur.age >= '18.0' AND	
	r.rating IS NOT NULL



-- Compute the cosine similarity between user --> 2.12 min
WITH UserBookRatings AS (
    SELECT
        uid as user_id,
        isbn,
        CAST(rating AS NUMERIC) AS rating
    FROM
        rating
),
UserRatingNorms AS (
    SELECT
        user_id,
        SQRT(SUM(rating * rating)) AS norm
    FROM
        UserBookRatings
    GROUP BY
        user_id
),
UserCosineSimilarities AS (
    SELECT
        ur1.user_id AS user1,
        ur2.user_id AS user2,
        CASE
            WHEN ua1.norm = 0 OR ua2.norm = 0 THEN 0  -- Handle division by zero
            ELSE SUM(ur1.rating * ur2.rating) / (ua1.norm * ua2.norm)
        END AS cosine_similarity
    FROM
        UserBookRatings ur1
    JOIN
        UserBookRatings ur2 ON ur1.isbn = ur2.isbn AND ur1.user_id < ur2.user_id
    JOIN
        UserRatingNorms ua1 ON ur1.user_id = ua1.user_id
    JOIN
        UserRatingNorms ua2 ON ur2.user_id = ua2.user_id
    GROUP BY
        ur1.user_id, ur2.user_id, ua1.norm, ua2.norm
)
SELECT
    user1,
    user2,
    cosine_similarity
FROM
    UserCosineSimilarities
WHERE cosine_similarity >= 0.6
ORDER BY
    user1, user2;
	

-- Get book of similar user according to the similarity score 75 ms
WITH book_of_target AS (
	SELECT isbn
	FROM rating
	WHERE uid = '119387'
),
similar_to_target AS (
	SELECT user1,user2 
	FROM similar_user 
	WHERE user1 = '119387' and score >= 0.7
	GROUP BY user1, user2	
),
book_of_similar AS (
	SELECT DISTINCT isbn
	FROM rating r
	JOIN similar_to_target stt ON user2 = r.uid
	WHERE isbn NOT IN (SELECT * FROM book_of_target)
)
SELECT b.isbn, title, author, year, publisher
FROM book b
JOIN book_of_similar bos ON bos.isbn = b.isbn
ORDER BY b.isbn DESC
