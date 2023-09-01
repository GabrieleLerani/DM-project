// Load Location.csv to create Location nodes
LOAD CSV WITH HEADERS FROM 'file:///Location.csv' AS row WITH row  WHERE row.Country IS NOT NULL
MERGE (location:Location {country: row.Country, province: row.Province});

// TODO test if it works, if yes remove LIVES_IN creation below
// Load location and user file and create a relation between user and book based on rating
CALL apoc.periodic.iterate(
  'LOAD CSV WITH HEADERS FROM "file:///Users_file.csv" AS row RETURN row',
  'MATCH (l:Location {country: row.Country, provence: row.Provence}) MERGE (user:User {userId: toInteger(row.`User-ID`), age:toFloat(row.Age))-[r:LIVES_IN]->(l);',
  { batchSize: 1000, parallel: false }
);

// Load book csv file and create book nodes
CALL apoc.periodic.iterate(
  'LOAD CSV WITH HEADERS FROM "file:///Books_file.csv" AS row RETURN row',
  'CREATE (book:Book {isbn: row.ISBN, title: row.`Book-Title`, author: row.`Book-Author`, year: row.`Year-Of-Publication`, publisher: row.Publisher})',
  { batchSize: 1000, parallel: false }
);

// Load rating csv and create a relation between user and book based on rating
CALL apoc.periodic.iterate(
  'LOAD CSV WITH HEADERS FROM "file:///Ratings_file.csv" AS row RETURN row',
  'MATCH (user:User {userId: toInteger(row.`User-ID`)}),(book:Book {isbn: row.ISBN}) MERGE (user)-[r:RATED {rating:toInteger(row.`Book-Rating`)}]->(book);',
  { batchSize: 1000, parallel: false }
);


// Create an index on location to avoid cartesian product
CREATE INDEX index_location IF NOT EXISTS FOR (l:Location) ON (l.country, l.province)

// Create relation between user and location
MATCH (user:User)
WHERE user.country IS NOT NULL AND user.province IS NOT NULL
WITH user
MERGE (location:Location {country: user.country, province: user.province})
MERGE (user)-[:LIVES_IN]->(location);




