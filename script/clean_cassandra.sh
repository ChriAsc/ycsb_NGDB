#!/bin/bash

# Define the keyspace and table names
KEYSPACE="ycsb"
TABLE="products"

# Build the CQL command
CQL_COMMAND="TRUNCATE $KEYSPACE.$TABLE;"

# Execute the CQL command using cqlsh
docker exec cassandra-3 cqlsh -e "$CQL_COMMAND"
