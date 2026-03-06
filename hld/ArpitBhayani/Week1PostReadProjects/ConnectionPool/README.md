# Connection Pool Demo

This small project demonstrates a basic JDBC connection pool and a tiny HTTP server to compare pooled vs direct connections using an in-memory H2 database.

Build and run (requires Java 17+ and Maven):

```bash
mvn package
java -jar target/connection-pool-0.1.0.jar
```

Endpoints:
- http://localhost:8080/direct - opens a new JDBC connection per request
- http://localhost:8080/pooled - reuses connections from the pool

You can run a simple benchmark with curl in a loop or use a load tester to compare the X-Duration-ms header returned.
