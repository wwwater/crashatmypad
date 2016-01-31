docker exec crashatmypad_postgres_1 createdb -U postgres crashpads
docker exec crashatmypad_postgres_1 psql -U postgres -c "CREATE USER crashatmypad WITH PASSWORD 'padmypad';"
docker exec crashatmypad_postgres_1 psql -U postgres -c "GRANT ALL PRIVILEGED ON DATABASE crashpads TO crashatmypad;"



docker exec -i -t crashatmypad_postgres_1 psql -U postgres -d crashpads
