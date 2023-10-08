import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

threads = [1, 2, 4, 6]

record_counts = [100000, 200000, 300000]

databases = ['cassandra', 'redis', 'mongodb']

workloads = ['read', 'insert', 'update']
wl_op_counts = {'read': [200000, 400000, 600000], 'insert': [10000, 25000, 50000], 'update': [20000, 40000, 60000]}
num_expected_fields = 3
# op_counts= [200000, 400000, 600000] # Read
# op_counts = [20000, 40000, 60000]   # Update
# op_counts = [10000, 25000, 50000]   # Insert

# Function to print a lineplot with databases' throughput, given the workload, nr. of operations, nr. of threads and nr. of records.
def print_throughput(workload):
    if workload == 'read':
        op_count = 200000
        thread = 1
        record_count = 100000
    elif workload == 'insert':
        op_count = 10000
        thread = 1
        record_count = 100000
    elif workload == 'update':
        op_count = 20000
        thread = 1
        record_count = 100000
    else:
        print("HAI SBAGLIATO IL PARAMETRO. Scegli un valore di workload pari alle stringhe \"read\", \"update\" o \"insert\"")
  
    # Reading from csv, this variable set the number of fields
    num_expected_fields = 3

    plt.figure()
    # Loop through the databases
    for database in databases:
        # Dataframe
        results = pd.read_csv(f"results/{database}/workload{workload}/output_run_{record_count}_{op_count}_{thread}.csv", names=['operation','timestamp(ms)','latency(us)'],low_memory=False)
        # Filtering only rows with 3 fields
        results = results[results.apply(lambda x: x.count() == num_expected_fields, axis=1)]
        results.columns= ['operation','timestamp(ms)','latency(us)']    # not necessary
        ts_result = results[results['operation'].str.contains(']') == False]
        # ts_result = results[:-66]   # to check
        # Since some headers are considered in read_csv, we filter them
        ts_result = ts_result[ts_result['timestamp(ms)']!=' timestamp(ms)']
        # Casting timestamp into float as it is convertend into datetime
        ts_result['timestamp(ms)'] = ts_result['timestamp(ms)'].astype(float)
        ts_result['timestamp(ms)'] = pd.to_datetime(ts_result['timestamp(ms)'], unit='ms')
        # Sorting values by timestamp
        ts_result.sort_values(by='timestamp(ms)')
        ts_result = ts_result[['operation', 'timestamp(ms)']]
        # Resampling second by second
        throughput_per_second = ts_result.resample('S', on='timestamp(ms)').agg({'operation':'count'})
        # Computing absolute time
        throughput_per_second['TimeElapsed'] = (throughput_per_second.index - throughput_per_second.index[0]).total_seconds()
        throughput_per_second['TimeElapsed'] = throughput_per_second['TimeElapsed'].astype(int)  # Cast to integers
        throughput_per_second = throughput_per_second.set_index('TimeElapsed')
        # Plotting
        sns.lineplot(data=throughput_per_second, legend='brief', label=database, x=throughput_per_second.index, y=throughput_per_second['operation'])
    plt.xlabel('seconds (sec)')
    plt.ylabel('throughput (ops/sec)')
    plt.title(f'Throughput: {op_count} operations, {thread} threads, {record_count} records')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    # plt.savefig(f"../Plots/Throughput_{record_count}_{op_count}_{thread}", bbox_inches='tight', dpi=500)
    print("Throughput Lineplot was successfully saved!")

# Function to print a heatmap with databases' throughput, given the workload, nr. of operation and vmin/vmax (for the map's scale).
def print_throughput_heatmap(workload, vmin, vmax):
    # Workload: "read", "insert", "update"
    if workload == "read":
        op_counts= [200000, 400000, 600000]
    elif workload == "update":
        op_counts = [20000, 40000, 60000]
    elif workload == "insert":
        op_counts = [10000, 25000, 50000]
    else:
        print("HAI SBAGLIATO IL PARAMETRO. Scegli un valore di workload pari alle stringhe \"read\", \"update\" o \"insert\"")

    # vmin = 1000000
    # vmax = 0
    # for database in databases:
    #     for record_count in record_counts:
    #         for op_count in op_counts:
    #             for thread in threads:
    #                 results = pd.read_csv(f"results/{database}/workload{workload}/output_run_{record_count}_{op_count}_{thread}.csv", skiprows=20, low_memory=False)
    #                 ts_result = results[-66:].reset_index(drop=True)
    #                 ts_result.columns= ['type','feature','value']
    #                 throughput=ts_result[ts_result['feature']==' Throughput(ops/sec)']['value'].values[0].strip()
    #                 if round(float(throughput))<vmin:
    #                     vmin = round(float(throughput))
    #                 if round(float(throughput))>vmax:
    #                     vmax = round(float(throughput)) + 1
    # print(f"Vmin for workload{workload}:\n{vmin}")
    # print(f"Vmax for workload{workload}:\n{vmax}")
                    
    fig, axes = plt.subplots(3,3,figsize=(10,10))
    i = 0

    for database in databases:
        for record_count in record_counts:
            # plt.figure()
            heatmap_df = pd.DataFrame(columns=['op_count', 'thread', 'throughput'])
            for op_count in op_counts:
                # To use this script, you need to adapt csv files, so that the first row is the dataframe's header
                for thread in threads:
                    results = pd.read_csv(f"results/{database}/workload{workload}/output_run_{record_count}_{op_count}_{thread}.csv", names=['operation','timestamp(ms)','latency(us)'],skiprows=20, low_memory=False)
                    # Throughput
                    ts_result = results[results['operation'].str.contains(']') == True]
                    ts_result = ts_result.reset_index(drop=True)
                    ts_result.columns= ['type','feature','value']
                    throughput=ts_result[ts_result['feature']==' Throughput(ops/sec)']['value'].values[0].strip()
                    # Complete dataframe
                    temp_heatmap_df = pd.DataFrame([[op_count, thread, throughput]], columns=['op_count', 'thread', 'throughput'])
                    heatmap_df = pd.concat([heatmap_df, temp_heatmap_df])
                    # print(heatmap_df)
            heatmap_df['throughput'] = pd.to_numeric(heatmap_df['throughput'], errors='coerce')
            heatmap_data = heatmap_df.pivot(index='thread', columns='op_count', values='throughput')
            row = i //  3
            col = i % 3
            ax = axes[row, col]
            i = i+1
            sns.heatmap(data=heatmap_data, ax=ax, annot=True, fmt=".1f", vmax=vmax, vmin=vmin, cmap='viridis')
            ax.set_title(f"{record_count} records, workload{workload}, {database}", fontsize=10)
    plt.tight_layout()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    # plt.savefig(f"../Plots/Heatmap_Throughput_{workload}", bbox_inches='tight', dpi=500)
    print("Throughput Heatmap was successfully saved!")


def print_latency_heatmap(workload, vmin, vmax):
    # Workload: "read", "insert", "update"
    if workload == "read":
        op_counts= [200000, 400000, 600000]
    elif workload == "update":
        op_counts = [20000, 40000, 60000]
    elif workload == "insert":
        op_counts = [10000, 25000, 50000]
    else:
        print("HAI SBAGLIATO IL PARAMETRO. Scegli un valore di workload pari alle stringhe \"read\", \"update\" o \"insert\"")

    # vmin = 1000000
    # vmax = 0
    # for database in databases:
    #     for record_count in record_counts:
    #         for op_count in op_counts:
    #             for thread in threads:
    #                 results = pd.read_csv(f"results/{database}/workload{workload}/output_run_{record_count}_{op_count}_{thread}.csv", names=['operation','timestamp(ms)','latency(us)'],skiprows=20, low_memory=False)
    #                 l_result = results[results['operation'].str.contains(']') == False]
    #                 l_result = l_result.reset_index(drop=True)

    #                 l_result = l_result[l_result['timestamp(ms)']!=' timestamp(ms)']
    #                 l_result = l_result[l_result['operation'] != 'CLEANUP']
    #                 latencies = l_result['latency(us)'].astype(int)
    #                 average = latencies.sum()/len(latencies)
    #                 if round(float(average))<vmin:
    #                     vmin = round(float(average))
    #                 if round(float(average))>vmax:
    #                     vmax = round(float(average)) + 1
    # print(f"Vmin for workload{workload}:\n{vmin}")
    # print(f"Vmax for workload{workload}:\n{vmax}")
                    
    fig, axes = plt.subplots(3,3,figsize=(10,10))
    i = 0

    for database in databases:
        for record_count in record_counts:
            # plt.figure()
            heatmap_df = pd.DataFrame(columns=['op_count', 'thread', 'latency'])
            for op_count in op_counts:
                # To use this script, you need to adapt csv files, so that the first row is the dataframe's header
                for thread in threads:
                    results = pd.read_csv(f"results/{database}/workload{workload}/output_run_{record_count}_{op_count}_{thread}.csv", names=['operation','timestamp(ms)','latency(us)'],skiprows=20, low_memory=False)
                    # Latency
                    l_result = results[results['operation'].str.contains(']') == False]
                    l_result = l_result.reset_index(drop=True)
                    # Since some headers are considered in read_csv, we filter them
                    l_result = l_result[l_result['timestamp(ms)']!=' timestamp(ms)']
                    l_result = l_result[l_result['operation'] != 'CLEANUP']
                    latencies = l_result['latency(us)'].astype(int)
                    average = latencies.sum()/len(latencies)
                    # Complete dataframe
                    temp_heatmap_df = pd.DataFrame([[op_count, thread, average]], columns=['op_count', 'thread', 'latency'])
                    heatmap_df = pd.concat([heatmap_df, temp_heatmap_df])
                    # print(heatmap_df)
            heatmap_df['latency'] = pd.to_numeric(heatmap_df['latency'], errors='coerce')
            heatmap_data = heatmap_df.pivot(index='thread', columns='op_count', values='latency')
            row = i //  3
            col = i % 3
            ax = axes[row, col]
            i = i+1
            sns.heatmap(data=heatmap_data, ax=ax, annot=True, fmt=".1f", vmax=vmax, vmin=vmin, cmap='viridis')
            ax.set_title(f"{record_count} records, workload{workload}, {database}", fontsize=10)
    plt.tight_layout()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    # plt.savefig(f"../Plots/Heatmap_Latency_{workload}", bbox_inches='tight', dpi=500)
    print("Latency Heatmap was successfully saved!")


def print_boxplot(workload):
    if workload == 'read':
        op_count = 200000
        thread = 1
        record_count = 100000
    elif workload == 'insert':
        op_count = 10000
        thread = 1
        record_count = 100000
    elif workload == 'update':
        op_count = 20000
        thread = 1
        record_count = 100000
    else:
        print("HAI SBAGLIATO IL PARAMETRO. Scegli un valore di workload pari alle stringhe \"read\", \"update\" o \"insert\"")
  
    # Reading from csv, this variable set the number of fields
    num_expected_fields = 3

    plt.figure()

    # Loop through the databases
    for database in databases:
        # Dataframe
        results = pd.read_csv(f"results/{database}/workload{workload}/output_run_{record_count}_{op_count}_{thread}.csv", names=['operation','timestamp(ms)','latency(us)'],low_memory=False)
        # Filtering only rows with 3 fields
        results = results[results.apply(lambda x: x.count() == num_expected_fields, axis=1)]
        results.columns= ['operation','timestamp(ms)','latency(us)']
        # ts_result = results[:-66]
        ts_result = results[results['operation'].str.contains(']') == False]
        ts_result = ts_result.reset_index(drop=True)
        # Since some headers are considered in read_csv, we filter them
        ts_result = ts_result[ts_result['timestamp(ms)']!=' timestamp(ms)']
        ts_result = ts_result[ts_result['operation']!='CLEANUP']
        ts_result = ts_result[['operation', 'latency(us)']]
        ts_result['latency(us)'] = ts_result['latency(us)'].astype(int)
        ts_result['database'] = database
        if database == 'mongodb':
            sns.boxplot(data=ts_result, x='database',y='latency(us)', legend='brief', hue='operation', log_scale=True)
            # sns.boxplot(data=ts_result, x='database',y='latency(us)', legend=False, log_scale=True) 
        else:
            # sns.boxplot(data=ts_result, x='database',y='latency(us)', legend=False, log_scale=True)
            sns.boxplot(data=ts_result, x='database',y='latency(us)', legend=False, hue='operation', log_scale=True)
    plt.xlabel('Database')
    plt.ylabel('Latency (us)')
    plt.title(f'Latencies\' boxplots: {op_count} operations, {thread} threads, {record_count} records')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    # plt.savefig(f"../Plots/Boxplot_Latency_{workload}", bbox_inches='tight', dpi=500)
    print("Latency Boxplot was successfully saved!")

def print_general_barplot():
    fig, axes = plt.subplots(1,3,figsize=(12,6))
    i=0
    
    for workload in workloads:
        runtimes_df = pd.DataFrame(columns=['workload', 'database', 'runtime(mean)', 'runtime(median)'])
        for database in databases:
            runtimes = np.array([])
            for record_count in record_counts:
                for op_count in wl_op_counts[workload]:
                    for thread in threads:
                        results = pd.read_csv(f"results/{database}/workload{workload}/output_run_{record_count}_{op_count}_{thread}.csv", names=['operation','timestamp(ms)','latency(us)'],low_memory=False)
                        # results = results[results.apply(lambda x: x.count() == num_expected_fields, axis=1)]
                        results.columns= ['operation','timestamp(ms)','latency(us)']
                        results = results[-200:]
                        ts_result = results[results['operation'].str.contains(']') == True]
                        ts_result = ts_result.reset_index(drop=True)
                        ts_result.columns= ['type','feature','value']
                        runtime=ts_result[ts_result['feature']==' RunTime(ms)']['value'].values[0].strip()
                        # Resampling to seconds
                        runtime=int(runtime)/1000
                        runtimes = np.append(runtimes, runtime)
            runtime_mean = np.mean(runtimes)
            runtime_median = np.median(runtimes)
            runtimes_df.loc[len(runtimes_df.index)] = [workload, database, runtime_mean, runtime_median]
            print(f"Workload{workload} successfully processed with {database}!")
        
        ax = axes[i]
        i = i+1
        sns.barplot(runtimes_df, ax=ax, x='workload', y='runtime(mean)', hue='database')
        ax.set_xlabel('Workload')
        ax.set_ylabel('Runtime (s)')
    fig.suptitle('Mean Runtime')
    plt.tight_layout()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    # plt.savefig(f"../Plots/Barplot_MeanRuntime_{workload}", bbox_inches='tight', dpi=500)
    print("Runtime Barplot was successfully saved!")




print_throughput_heatmap("read", vmin=800, vmax=10000)
print_throughput_heatmap("update", vmin=1400, vmax=24000)
print_throughput_heatmap("insert", vmin=1000, vmax=16000)

print_latency_heatmap("read", vmin=200, vmax=2500)
print_latency_heatmap("update", vmin=0, vmax=1600)
print_latency_heatmap("insert", vmin=100, vmax=2100)

print_throughput("read")
print_throughput("update")
print_throughput("insert")

print_boxplot("read")
print_boxplot("update")
print_boxplot("insert")

print_general_barplot()


plt.show()
print('ok')