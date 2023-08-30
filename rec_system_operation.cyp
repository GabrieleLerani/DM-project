// Import Location.csv to create Location nodes
LOAD CSV WITH HEADERS FROM 'file:///Location.csv' AS row WITH row  WHERE row.Country IS NOT NULL
MERGE (location:Location {country: row.Country, province: row.Province});

LOAD CSV WITH HEADERS FROM 'file:///Users_file.csv' AS row
CREATE (user:User {userId: toInteger(row.`User-ID`), age:toFloat(row.Age),country: row.Country,province:row.Province});

LOAD CSV WITH HEADERS FROM 'file:///Ratings_file.csv' AS row
CREATE (rating:Rating {userId: toInteger(row.`User-ID`), isbn: row.ISBN, rating: row.`Book-Rating`});



// Create an index on location to avoid cartesian product
CREATE INDEX index_location IF NOT EXISTS FOR (l:Location) ON (l.country, l.province)

// Split the query execution and leverages index to speed up 
MATCH (user:User)
WHERE user.country IS NOT NULL AND user.province IS NOT NULL
WITH user
MERGE (location:Location {country: user.country, province: user.province})
MERGE (user)-[:LIVES_IN]->(location);