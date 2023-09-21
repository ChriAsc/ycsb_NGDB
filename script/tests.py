import subprocess
import os
import sys

threads = [1, 2, 4, 6]
record_counts = [100000, 200000, 300000]
def main(database, workload, op_counts):
    if database == "mongodb":
        load_command_start = f"../ycsb-{database}-binding-0.18.0-SNAPSHOT/bin/ycsb.sh load {database} -s -P ../workloads/workload{workload} -p mongodb.url=mongodb://127.0.0.1:27017/ycsb?retryWrites=true "
        run_command_start = f"../ycsb-{database}-binding-0.18.0-SNAPSHOT/bin/ycsb.sh run {database} -s -P ../workloads/workload{workload} -p mongodb.url=mongodb://127.0.0.1:27017/ycsb?retryWrites=true "
        load_command = f"../ycsb-{database}-binding-0.18.0-SNAPSHOT/bin/ycsb.sh load {database} -s -P ../workloads/workload{workload} -p mongodb.url=mongodb://127.0.0.1:27017/ycsb?retryWrites=true "
        run_command = f"../ycsb-{database}-binding-0.18.0-SNAPSHOT/bin/ycsb.sh run {database} -s -P ../workloads/workload{workload} -p mongodb.url=mongodb://127.0.0.1:27017/ycsb?retryWrites=true "
        cleanup_command = "mongosh < mongoclean.mongodb"
    elif database == "cassandra":
        load_command = f"../ycsb-{database}-binding-0.18.0-SNAPSHOT/bin/ycsb.sh load {database}2-cql -s -P ../workloads/workload{workload} -p hosts=127.0.0.1"
        run_command = f""
        cleanup_command = f""
    elif database == "redis":
        load_command = f"../ycsb-{database}-binding-0.18.0-SNAPSHOT/bin/ycsb.sh load {database} -s -P workloads/workload{workload} -p \"redis.host=127.0.0.1\" -p \"redis.port=6379\""
        run_command = f"../ycsb-{database}-binding-0.18.0-SNAPSHOT/bin/ycsb.sh run {database} -P workloads/workload{workload} -p \"redis.host=127.0.0.1\" -p \"redis.port=6379\""
        cleanup_command = "docker exec -it redis-container redis-cli FLUSHALL"
    else:
        print("ERRORE. NOME DEL DATABASE ERRATO. PER FAVORE USA \"mongodb\" \"cassandra\" o \"redis\"")
    for record_count in record_counts:
        load_command += f"-p recordcount={record_count}"
        result_load = subprocess.run(load_command.split(' '), capture_output=True, text=True)
        print(f"Loaded {record_count} records to databse successfully")
        with open(f"../results/{database}/workload{workload}/output_load_{record_count}.txt", "w") as fin:
            fin.write(result_load.stdout)
        for op_count in op_counts:
            for thread in threads:
                run_command += f"-p operationcount={op_count} -threads {thread}"
                result_write = subprocess.run(run_command.split(' '), capture_output=True, text=True)
                print(f"Runned tests with {record_count} records, {op_count} operation and {thread} threads against databse successfully")
                with open(f"../results/{database}/workload{workload}/output_run_{record_count}_{op_count}_{thread}.txt", 'w') as fin2:
                    fin2.write(result_write.stdout)
                run_command = run_command_start
        subprocess.run(cleanup_command.split(' '))
        print("Cleanup executed correctly")
        load_command = load_command_start
        
        

if __name__=="__main__":
    database = sys.argv[1]
    workload = sys.argv[2]
    if workload == "read":
        op_counts= [200000, 400000, 600000]
    elif workload == "update":
        op_counts = [20000, 40000, 60000]
    elif workload == "update":
        op_counts = [10000, 25000, 50000]
    else:
        print("HAI SBAGLIATO IL PARAMETRO. Scegli un valore di workload pari alle stringhe \"read\", \"update\" o \"insert\"")
        exit(1)
    main(database, workload, op_counts)