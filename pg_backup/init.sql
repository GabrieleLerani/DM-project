-- Create the database (if not already created)
CREATE DATABASE dmproject;

-- Connect to the database
\c dmproject;

-- Restore data from the binary backup file using pg_restore
\! pg_restore -d dmproject -U postgres /docker-entrypoint-initdb.d/pg;
