# Comparison between Relational DBMS as PostgreSQL and a NoSQL tool as Neo4j
![Screenshot from 2024-03-03 22-31-54](https://github.com/GabrieleLerani/DM-project/assets/92364167/f75a8eb9-7db4-4506-b9a8-49de2214a5ab)

Relational databases are useful when dealing with structured data and well-defined relationships, providing a strong schema and supporting 
complex queries through SQL. They are often employed in scenarios requiring data integrity, ACID compliance, and established transactional 
processes, such as financial systems.

On the other hand, NoSQL databases, including graph databases like Neo4j, are beneficial in situations where data structures are dynamic, and relationships 
are a focal point. They offer flexibility, scalability, and excel in handling unstructured or semi-structured data, making them suitable for applications like social networks, recommendation systems, and scenarios where relationships play a critical role. 

# Dataset 
Book dataset: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?select=Ratings.csv

# Goal
![Screenshot from 2024-03-04 10-10-42](https://github.com/GabrieleLerani/DM-project/assets/92364167/dcfabfbb-23aa-4a14-8787-05390a01313b)

The goal of the project is to carry out a comparison between PostgreSQL and Neo4j. To accomplish the task I built a recommendation system over a real book dataset whose
structure seems to fit a graph well (e.g. there is an edge between a user node and a book node if the user has read the book). In neo4j this task can be accomplished
with aggregate functions and machine learning module of the Neo4j Graph Data Science Library as FastRP and kNN. These functions operate directly on the graph database 
without the need to extract data via queries and process them subsequently. On the other hand in PostgreSQL is not possible
to do the same type of operations directly on the data, but you need to extract them and build a Neural Network to realize a recommendation system.

# Implementation
![Screenshot from 2024-03-04 14-13-16](https://github.com/GabrieleLerani/DM-project/assets/92364167/b5d22dd5-4ddd-42e0-b74f-01884bc4f7dc)

In order to interact with the recommendation system I implemented a simple webapp using flask where you can type the user id and it returns the list of suggested books based on similarities between user with same preferences.

# Usage
Run the following command once you have created the docker image from the dockerfile:
`docker run --name webapp -p 5001:5001 -e DB_TYPE=NEO4J --network host dm-webapp`

# Results
![query-response-time](https://github.com/GabrieleLerani/DM-project/assets/92364167/93a4ca05-d089-4148-8c48-1e35115c0318)

The results show how Graph databases like Neo4j are particularly well-suited for scenarios where relationships between data are crucial, they also provide
better scalability with more users. On the other side when you need a predefined organization of data Relation DBMS are the best choices.

