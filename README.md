# Comparison between Relational DBMS as PostgreSQL and a NoSQL tool as Neo4j
Relational databases are useful when dealing with structured data and well-defined relationships, providing a strong schema and supporting 
complex queries through SQL. They are often employed in scenarios requiring data integrity, ACID compliance, and established transactional 
processes, such as financial systems.

On the other hand, NoSQL databases, including graph databases like Neo4j, are beneficial in situations where data structures are dynamic, and relationships 
are a focal point. They offer flexibility, scalability, and excel in handling unstructured or semi-structured data, making them suitable for applications like social networks, recommendation systems, and scenarios where relationships play a critical role. 

# Dataset 
Book dataset: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?select=Ratings.csv

# Goal
The goal of the project is to carry out a comparison between PostgreSQL and Neo4j. To accomplish the task I built a recommendation system over a real book dataset whose
structure seems to fit a graph well (e.g. there is an edge between a user node and a book node if the user has read the book). In neo4j this task can be accomplished
with aggregate functions and machine learning module of the Neo4j Graph Data Science Library as FastRP and kNN. These functions operate directly on the graph database 
without the need to extract data via queries and process them subsequently. On the other hand in PostgreSQL is not possible
to do the same type of operations directly on the data, but you need to extract them and build a Neural Network to realize a recommendation system.

# Results
The results show how Graph databases like Neo4j are particularly well-suited for scenarios where relationships between data are crucial, they also provide
better scalability with more users. On the other side when you need a predefined organization of data Relation DBMS are the best choices.

