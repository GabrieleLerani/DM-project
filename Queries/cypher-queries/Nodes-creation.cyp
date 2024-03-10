// 1 - Load Location.csv to create Location nodes
LOAD CSV WITH HEADERS FROM 'file:///Location.csv' AS row WITH row  WHERE row.Country IS NOT NULL and row.Province IS NOT NULL
MERGE (location:Location {country: row.Country, province: row.Province});


// 2 - Load location and user file and create a relation between user and book based on rating, it also removes user without age
:auto LOAD CSV WITH HEADERS FROM "file:///Users_file.csv" AS row 
CALL {
  WITH row
  MATCH (l:Location {country: row.Country, province: row.Province}) 
  MERGE (user:User {userId: toInteger(row.`User-ID`)})-[r:LIVES_IN]->(l)
   ON CREATE SET user.age = row.Age
   
} IN TRANSACTIONS OF 10000 ROWS


// 3 - Load book csv file and create book nodes
:auto LOAD CSV WITH HEADERS FROM "file:///Books_file.csv" AS row 
CALL {
  WITH row
  CREATE (book:Book {isbn: row.ISBN, title: row.`Book-Title`, author: row.`Book-Author`, year: row.`Year-Of-Publication`, publisher: row.Publisher})
  
} IN TRANSACTIONS OF 10000 ROWS


// 4 - Create a relationship between user and book that have rated that book
:auto LOAD CSV WITH HEADERS FROM "file:///Ratings_file.csv" AS row 
CALL {
  WITH row
  MATCH (user:User {userId: toInteger(row.`User-ID`)}),(book:Book {isbn: row.ISBN}) 
  MERGE (user)-[r:RATED {rating:toInteger(row.`Book-Rating`)}]->(book)
} IN TRANSACTIONS OF 10000 ROWS


// 5 - Remove users that have not rated a book
:auto CALL {
    MATCH (node:User)
    WHERE NOT EXISTS((node)-[:RATED]->())
    DETACH DELETE node
} IN TRANSACTIONS OF 10000 ROWS



// Create test user with random id and a test flag
CREATE (u:User)
SET  u.age = toInteger(rand() * 100), u.test = True,
     u.userId = toInteger(rand() * (290000 - 300000 + 1)) + 300000
      
// Create for the newly added user a RATED relationship with 3 random books
WITH u
MATCH (b:Book)
WITH b, RAND() AS random, u
ORDER BY random LIMIT 3
WITH b, u
CREATE (u)-[r:RATED]->(b)
SET r.rating = toInteger(rand() * 10), r.test = True


// Delete test nodes along with their relationships
MATCH (u)-[:RATED]->() WHERE u.test = True DETACH DELETE u


// Most efficent way to remove nodes
CALL apoc.periodic.iterate(
  "MATCH (r:User) RETURN r",
  "DELETE r",
  {batchSize:1000, parallel:true})