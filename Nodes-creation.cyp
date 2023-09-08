// Load Location.csv to create Location nodes
LOAD CSV WITH HEADERS FROM 'file:///Location.csv' AS row WITH row  WHERE row.Country IS NOT NULL and row.Province IS NOT NULL
MERGE (location:Location {country: row.Country, province: row.Province});


// Load location and user file and create a relation between user and book based on rating, it also removes user without age
LOAD CSV WITH HEADERS FROM "file:///Users_file.csv" AS row 
:auto CALL {
  WITH row
  MATCH (l:Location {country: row.Country, province: row.Province}) 
  MERGE (user:User {userId: toInteger(row.`User-ID`)})-[r:LIVES_IN]->(l)
   ON CREATE SET user.age = row.Age
   
} IN TRANSACTIONS OF 10000 ROWS


// Load book csv file and create book nodes
LOAD CSV WITH HEADERS FROM "file:///Books_file.csv" AS row 
:auto CALL {
  WITH row
  CREATE (book:Book {isbn: row.ISBN, title: row.`Book-Title`, author: row.`Book-Author`, year: row.`Year-Of-Publication`, publisher: row.Publisher})
  
} IN TRANSACTIONS OF 10000 ROWS


// Create a relationship between user and book that have rated that book
LOAD CSV WITH HEADERS FROM "file:///Ratings_file.csv" AS row 
:auto CALL {
  WITH row
  MATCH (user:User {userId: toInteger(row.`User-ID`)}),(book:Book {isbn: row.ISBN}) 
  MERGE (user)-[r:RATED {rating:toInteger(row.`Book-Rating`)}]->(book)
} IN TRANSACTIONS OF 10000 ROWS


// Remove users that have not rated a book
:auto CALL {
    MATCH (node:User)
    WHERE NOT EXISTS((node)-[:RATED]->())
    DETACH DELETE node
} IN TRANSACTIONS OF 10000 ROWS




