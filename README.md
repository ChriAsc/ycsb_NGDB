Yahoo Cloud Serving Benchmark (NGDB)
====================================
[![Docs](https://img.shields.io/badge/docs-reference-blue.svg)](https://github.com/brianfrankcooper/YCSB/wiki)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](https://github.com/ChriAsc/ycsb_NGDB/blob/main/LICENSE.txt)

This project is dedicated to benchmarking some of the most popular NoSQL databases, including Redis, MongoDB and Cassandra, using the Yahoo! Cloud Serving Benchmark (YCSB).


Overview
--------

*YCSB* is an open-source benchmarking tool created by Yahoo! to assess the performance of various NoSQL databases. It provides a standardized framework for testing the scalability and performance of different data stores under realistic workloads. This project mainly uses a *products* table and aach product in this table contains essential information, including its name, availability, price and description. Three distinct workloads were defined to assess different database scenarios.

In this repository, we focus on benchmarking three prominent NoSQL databases:
- Redis: an in-memory data store used for caching and high-speed data access.
- MongoDB: a powerful document-oriented database known for its flexibility and scalability.
- Cassandra: a distributed, highly available and scalable NoSQL database designed for handling large amounts of data.


Table Structure
---------------

- The *products* table represents a simplified e-commerce product catalog, with the following schema:
    - Name: the name of the product.
    - Availability: whether the product is in stock (true/false).
    - Price: the price of the product.
    - Description: a brief description of the product.

- Workloads:

    - Read-Only Workload: this workload focuses on read operations and is designed to simulate scenarios where users are browsing product listings. It consists mainly of read operations to retrieve product information.
    - Balanced Read and Update Workload: in this workload, we strike a balance between read and update operations. It simulates scenarios where users not only view products, but also modify product availability or prices. This workload includes a mix of read and update operations.
    - Update and Insert Workload: it is geared towards assessing the database's ability to handle frequent updates and new product additions. It includes operations to update product availability and add new products to the catalog.

Key Features
------------

- Benchmarking Configurations: we provide pre-configured YCSB benchmarking scenarios for Redis, MongoDB and Cassandra. These configurations are designed to simulate real-world use cases and can be easily customized to fit your specific requirements.
- Performance Metrics: track essential performance metrics such as throughput, latency and resource utilization for each database during benchmarking.
- Comprehensive Documentation: our repository includes detailed documentation on how to set up, configure and run YCSB benchmarks for Redis, MongoDB and Cassandra.


Getting Started
---------------

1. Download the [latest release of ycsb_NGDB](https://github.com/ChriAsc/ycsb_NGDB/releases):

    ```sh
    curl -O --location https://github.com/ChriAsc/ycsb_NGDB/releases/...
    tar xfvz ...
    cd ...
    ```
    
2. Set up a database to benchmark. There is a README file under each binding directory.

3. Run YCSB command. 

    On Linux:
    ```sh
    bin/ycsb.sh load basic -P workloads/workloada
    bin/ycsb.sh run basic -P workloads/workloada
    ```

    On Windows:
    ```bat
    bin/ycsb.bat load basic -P workloads\workloada
    bin/ycsb.bat run basic -P workloads\workloada
    ```

  Running the `ycsb` command without any argument will print the usage. 
   
  <sub>See https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload for a detailed documentation on how to run a workload.</sub>
  
  <sub>See https://github.com/brianfrankcooper/YCSB/wiki/Core-Properties for the list of available workload properties.</sub>


Building from source
--------------------

YCSB requires the use of Maven 3; if you use Maven 2, you may see [errors
such as these](https://github.com/brianfrankcooper/YCSB/issues/406).

To build the full distribution, with all database bindings:

    mvn clean package

To build a single database binding:

    mvn -pl site.ycsb:mongodb-binding -am clean package


Links
-----
* [Original project docs](https://github.com/brianfrankcooper/YCSB/wiki)
* [The original announcement from Yahoo!](https://labs.yahoo.com/news/yahoo-cloud-serving-benchmark/)

<sub>In this repository, we have imported and used files from the [YCSB (Yahoo Cloud Serving Benchmark)](https://github.com/brianfrankcooper/YCSB) project. YCSB is a popular benchmarking tool for evaluating the performance of various NoSQL databases and cloud-based datastores. Please, refer to their wiki for more information. </sub> 
