# Yahoo Cloud Serving Benchmark (NGDB)

[![Docs](https://img.shields.io/badge/docs-reference-blue.svg)](https://github.com/brianfrankcooper/YCSB/wiki)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](https://github.com/ChriAsc/ycsb_NGDB/blob/main/LICENSE.txt)

This project is dedicated to benchmarking some of the most popular NoSQL databases, including Redis, MongoDB and Cassandra, using the Yahoo! Cloud Serving Benchmark (YCSB).


## Overview

*YCSB* is an open-source benchmarking tool created by Yahoo! to assess the performance of various NoSQL databases. It provides a standardized framework for testing the scalability and performance of different data stores under realistic workloads. This project mainly uses a *products* table and aach product in this table contains essential information, including its name, price, availability, description and category. Three distinct workloads were defined to assess different database scenarios.

In this repository, we focus on benchmarking three prominent NoSQL databases:
- [Redis](https://redis.io): an in-memory data store used for caching and high-speed data access;
- [MongoDB](https://www.mongodb.com): a powerful document-oriented database known for its flexibility and scalability;
- [Cassandra](https://cassandra.apache.org/_/index.html): a distributed, highly available and scalable NoSQL database designed for handling large amounts of data.


## Table Structure

- The *products* table represents a simplified e-commerce product catalog, with the following schema:
    - Name: the name of the product;
    - Price: the price of the product;
    - Availability: whether the product is in stock (true/false);
    - Description: a brief description of the product;
    - Category: the category or type of the product.

- Workloads:

    - Read-heavy Workload: this workload predominantly focuses on read operations, simulating scenarios where users browse product listings; moreover, it also includes occasional updates to product availability, prices or other attributes (90% Read, 10% Update).
    - Mixed Workload: it combines various read-modify-write, read, and write operations to mimic a mix of user interactions; Read-Modify-Write (60%) represents operations where users modify product details (e.g. updating availability or price), Read (30%) simulates read-heavy operations as users browse product listings, Write (10%) represents operations where new products are added.
    - Update-Intensive Workload: it assesses the database's ability to handle frequent updates to product information and it includes a balance of read and write operations, simulating scenarios where products are frequently updated, read and added (70% Update, 15% Read, 15% Write).

## Key Features

- Benchmarking Configurations: we provide pre-configured YCSB benchmarking scenarios for Redis, MongoDB and Cassandra. These configurations are designed to simulate real-world use cases and can be easily customized to fit your specific requirements.
- Performance Metrics: track essential performance metrics such as throughput, latency and resource utilization for each database during benchmarking.
- Comprehensive Documentation: our repository includes detailed documentation on how to set up, configure and run YCSB benchmarks for Redis, MongoDB and Cassandra.


## Getting Started

### 1. Start DB instance
You can also run a Docker container. [Docker](https://www.docker.com/) is a containerization platform that allows you to run applications, including databases, in isolated environments called containers. 

### 2. Install Java and Maven
YCSB requires the use of Maven 3; if you use Maven 2, you may see [errors such as these](https://github.com/brianfrankcooper/YCSB/issues/406).

### 3. Set Up YCSB
Download the [latest release of ycsb_NGDB](https://github.com/ChriAsc/ycsb_NGDB/releases):

    git clone https://github.com/ChriAsc/ycsb_NGDB
    cd ycsb_NGDB
    
    
### 4. Building from source
Set up a database to benchmark. There is a README file under each binding directory.

To build the full distribution, with all database bindings:

    mvn clean package

To build a single database binding:

    mvn -pl site.ycsb:DB-binding -am clean package
    
<sub>*Replace "DB" with database name, e.g. "redis"*</sub>

### 5. Run YCSB command
You can provide DB Connection Parameters or set configs with the shell command.

    On Linux:
    bin/ycsb.sh load redis -s -P workloads/workloada -p "redis.host=127.0.0.1" -p "redis.port=6379" > outputLoad.txt
    bin/ycsb.sh run  redis -s -P workloads/workloada -p "redis.host=127.0.0.1" -p "redis.port=6379" > outputRun.txt

    
    On Windows:
    bin/ycsb.bat load redis -s -P workloads/workloada -p "redis.host=127.0.0.1" -p "redis.port=6379" > outputLoad.txt
    bin/ycsb.bat run  redis -s -P workloads/workloada -p "redis.host=127.0.0.1" -p "redis.port=6379" > outputRun.txt

  Running the `ycsb` command without any argument will print the usage. 
   
  <sub>See https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload for a detailed documentation on how to run a workload.</sub>
  
  <sub>See https://github.com/brianfrankcooper/YCSB/wiki/Core-Properties for the list of available workload properties.</sub>


Links
-----

* [Original project docs](https://github.com/brianfrankcooper/YCSB/wiki)
* [The original announcement from Yahoo!](https://labs.yahoo.com/news/yahoo-cloud-serving-benchmark/)

<sub>In this repository, we have imported and used files from the [YCSB (Yahoo Cloud Serving Benchmark)](https://github.com/brianfrankcooper/YCSB) project. YCSB is a popular benchmarking tool for evaluating the performance of various NoSQL databases and cloud-based datastores. Please, refer to their wiki for more information. </sub> 
