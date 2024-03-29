// Create the graph projection to allow GDS algorithm execution
CALL gds.graph.project(
    'embedding-projection',
    ['User','Book'],
    {
        RATED:{
            orientation: 'UNDIRECTED',
            properties: 'rating'
        }
    }
);

// Create node embedding and write on Neo4j graph
CALL gds.fastRP.write(
  'embedding-projection',
  {
    embeddingDimension: 32,
    randomSeed:42,
    writeProperty: 'embedding',
    relationshipWeightProperty: 'rating'
  }
)
YIELD nodePropertiesWritten;

// Create a new projection with the new embedded property for all relation (wildcard)
CALL gds.graph.project(
    'books_embedding',
    {
        User: {properties:'embedding'}
        //Book: {properties:'embedding'}
    },
    '*'
);

// run KNN to estimate similarity (a.k.a. SIMILAR) relationships 
// between users rated books and write them back to the graph
CALL gds.knn.write('books_embedding', {
    nodeLabels: ['User'],
    nodeProperties: ['embedding'],
    concurrency: 4,
    sampleRate: 1.0,
    deltaThreshold: 0.0,
    writeRelationshipType: "SIMILAR",
    writeProperty: "score",
    maxIterations: 200
})
YIELD nodesCompared, relationshipsWritten, similarityDistribution
RETURN nodesCompared, relationshipsWritten, similarityDistribution.mean as meanSimilarity;

// Get similar user for a target user
MATCH (targetUser:User {userId: 67932})-[r:SIMILAR]->(similarUser:User)
RETURN similarUser.userId as UID, r.score as similarity
ORDER BY similarity DESCENDING

// Get similar user from the same location of the target user
MATCH (l1:Location)<-[lives1:LIVES_IN]-(targetUser:User {userId: 67932})-[r:SIMILAR]->(similarUser:User)-[lives2:LIVES_IN]->(l2:Location)
WHERE l1.country = l2.country AND r.score >= 0.6
RETURN similarUser.userId as UID, r.score as similarity, l1.country as country
ORDER BY similarity DESCENDING, UID, country

// Get the ratio between the user coming from the same location and the total amount of similar user for a target user
MATCH (l1:Location)<-[lives1:LIVES_IN]-(targetUser:User {userId: 67932})-[s:SIMILAR]->(similarUser:User)-[lives2:LIVES_IN]->(l2:Location)
WHERE l1.country = l2.country AND s.score >= 0.6
WITH COUNT(*) as similarUserFromSameLocationCount
MATCH (targetUser:User {userId: 67932})-[:SIMILAR]->(similarUser:User)
WITH similarUserFromSameLocationCount, COUNT(similarUser) as similarUserCount
RETURN toFloat(similarUserFromSameLocationCount) / toFloat(similarUserCount) as similarUserCountryRatio


// Get the ratio between the user coming from the same location and the total amount of similar user for all the user
// Useful to understand similarities based on country and user location, to filter by user insert user id in first line
MATCH (l1:Location)<-[lives1:LIVES_IN]-(targetUser:User)-[s:SIMILAR]->(similarUser:User)-[lives2:LIVES_IN]->(l2:Location)
WHERE l1.country = l2.country AND l1.province = l2.province AND s.score >= 0.6
WITH COUNT(*) as similarUserFromSameLocationCount, targetUser as u1, l1 
MATCH (targetUser:User {userId: u1.userId})-[s:SIMILAR]->(similarUser:User)
WHERE s.score >= 0.6
WITH similarUserFromSameLocationCount, COUNT(similarUser) as similarUserCount, u1.userId as uid, l1.country as country, l1.province as province
RETURN country,province, uid, toFloat(similarUserFromSameLocationCount) / toFloat(similarUserCount) as similarUserCountryRatio
ORDER BY similarUserCountryRatio DESC LIMIT 200

// Get the ratio of users having more than 60 % of similar user coming from the same country
MATCH (l1:Location)<-[lives1:LIVES_IN]-(targetUser:User)-[s:SIMILAR]->(similarUser:User)-[lives2:LIVES_IN]->(l2:Location)
WHERE l1.country = l2.country AND s.score >= 0.6
WITH COUNT(*) as similarUserFromSameLocationCount, targetUser as u1, l1 
MATCH (targetUser:User {userId: u1.userId})-[s:SIMILAR]->(similarUser:User)
WHERE s.score >= 0.6
WITH similarUserFromSameLocationCount, COUNT(similarUser) as similarUserCount, u1.userId as uid, l1.country as country
WITH country, uid, toFloat(similarUserFromSameLocationCount) / toFloat(similarUserCount) as similarUserCountryRatio
WHERE similarUserCountryRatio >= 0.6
WITH COUNT(uid) as userWithSimilarInSameLocation
MATCH (n:User)
WITH COUNT(n) as allUser, userWithSimilarInSameLocation
RETURN toFloat(userWithSimilarInSameLocation)/toFloat(allUser) as ratio


// Get suggested book according to similarity score for a given user
MATCH (targetUser:User {userId: 119274})-[similar:SIMILAR]->(similarUser:User)-[rated:RATED]->(b:Book)
WHERE similar.score >= 0.6
WITH COLLECT(DISTINCT b.title) as similarBooks
UNWIND similarBooks as books
RETURN books ORDER BY books.title

