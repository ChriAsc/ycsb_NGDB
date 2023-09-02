YCSB
====================================
[![Docs](https://img.shields.io/badge/docs-reference-blue.svg)](https://github.com/brianfrankcooper/YCSB/wiki)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](https://github.com/ChriAsc/ycsb_NGDB/blob/main/LICENSE.txt)

<sub>In this repository, we have imported and used files from the [YCSB (Yahoo Cloud Serving Benchmark)](https://github.com/brianfrankcooper/YCSB) project. YCSB is a popular benchmarking tool for evaluating the performance of various NoSQL databases and cloud-based datastores. Please, refer to their wiki for more information.</sub> 

Getting Started
---------------

1. Download the [latest release of YCSB](https://github.com/ChriAsc/ycsb_NGDB/releases):

    ```sh
    curl -O --location https://github.com/ChriAsc/ycsb_NGDB/releases/...
    tar xfvz ...
    cd ...
    ```
    
2. Set up a database to benchmark. There is a README file under each binding 
   directory.

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
   
  See https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
  for a detailed documentation on how to run a workload.

  See https://github.com/brianfrankcooper/YCSB/wiki/Core-Properties for 
  the list of available workload properties.


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
