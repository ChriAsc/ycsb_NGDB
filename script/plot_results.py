import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


threads = [1, 2, 4, 6]

record_counts = [100000, 200000, 300000]
op_counts= [200000, 400000, 600000] # Read
# op_counts = [20000, 40000, 60000]   # Update
# op_counts = [10000, 25000, 50000]   # Insert

def print_throughput():
    for op_count in op_counts:
        # To use this script, you need to adapt csv files, so that the first row is the dataframe's header
        for thread in threads:
            plt.figure()

            results = pd.read_csv(f"results/cassandra/workloadread/output_run_100000_{op_count}_{thread}.csv", header=0, low_memory=False)
            results.columns= ['operation','timestamp(ms)','latency(us)']
            ts_result = results[:-66]
            ts_result = ts_result[ts_result['timestamp(ms)']!=' timestamp(ms)']
            ts_result['timestamp(ms)'] = pd.to_datetime(ts_result['timestamp(ms)'], unit='ms')
            ts_result.sort_values(by='timestamp(ms)')
            ts_result = ts_result[['operation', 'timestamp(ms)']]
            throughput_per_second = ts_result.resample('S', on='timestamp(ms)').agg({'operation':'count'})
            throughput_per_second['TimeElapsed'] = (throughput_per_second.index - throughput_per_second.index[0]).total_seconds()
            throughput_per_second['TimeElapsed'] = throughput_per_second['TimeElapsed'].astype(int)  # Cast to integers
            throughput_per_second = throughput_per_second.set_index('TimeElapsed')

            sns.lineplot(data=throughput_per_second, x=throughput_per_second.index, y=throughput_per_second['operation']).set(title=f'{op_count}_{thread}')

    plt.show()

def print_heatmap():
    for record_count in record_counts:
        plt.figure()
        heatmap_df = pd.DataFrame(columns=['op_count', 'thread', 'throughput'])
        for op_count in op_counts:
            # To use this script, you need to adapt csv files, so that the first row is the dataframe's header
            for thread in threads:
                results = pd.read_csv(f"results/cassandra/workloadread/output_run_{record_count}_{op_count}_{thread}.csv", skiprows=20, low_memory=False)
                ts_result = results[-66:].reset_index(drop=True)
                ts_result.columns= ['type','feature','value']
                throughput=ts_result[ts_result['feature']==' Throughput(ops/sec)']['value'].values[0].strip()
                temp_heatmap_df = pd.DataFrame([[op_count, thread, throughput]], columns=['op_count', 'thread', 'throughput'])
                heatmap_df = pd.concat([heatmap_df, temp_heatmap_df])
                print(heatmap_df)
        heatmap_df['throughput'] = pd.to_numeric(heatmap_df['throughput'], errors='coerce')
        heatmap_data = heatmap_df.pivot('thread', 'op_count', 'throughput')
        sns.heatmap(data=heatmap_data)
        plt.show()

print_heatmap()


