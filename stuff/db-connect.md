# Connecting to Postgres Database

## Dev (Postgres Instance)

``` bash
psql \
-h dev.c7umrsreh09y.us-east-1.rds.amazonaws.com \
-U serve_db \
-d video_db
```

## Aurora Serverless (Postgres)

``` bash
psql \
-h serve-db-cluster.cluster-c7umrsreh09y.us-east-1.rds.amazonaws.com \
-U serve_db \
-d video_db
```