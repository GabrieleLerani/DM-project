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
)

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
YIELD nodePropertiesWritten

// Create a new projection with the new embedded property for all relation (wildcard)
CALL gds.graph.project(
    'books_embedding',
    {
        User: {properties:'embedding'},
        Book: {properties:'embedding'}
    },
    '*'
)

// run KNN to estimate similarity (a.k.a. SIMILAR) relationships 
// between users articles and write them back to the graph
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
RETURN nodesCompared, relationshipsWritten, similarityDistribution.mean as meanSimilarity

// Get similar user for a target user
MATCH (targetUser:User {userId: 9659})-[r:SIMILAR]->(similarUser:User)
RETURN targetUser.userId as person1, similarUser.userId as person2, r.score as similarity
ORDER BY similarity DESCENDING, person1, person2 

// Get suggested book according to similarity score for a given user
MATCH (targetUser:User {userId: 9659})-[similar:SIMILAR]->(similarUser:User)
WHERE similar.score > 0.9
WITH targetUser, similarUser, similar
MATCH (similarUser)-[rated:RATED]->(b:Book)
RETURN targetUser.userId as targetUser, COLLECT(DISTINCT b.title) as SuggestedBook   