import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_theme()

# full_reads_fast = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])
# full_reads_normal = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])
# full_reads_slow = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])

# full_scans_fast = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])
# full_scans_normal = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])
# full_scans_slow = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])

# full_updates_fast = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])
# full_updates_normal = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])
# full_updates_slow = pd.DataFrame(columns=['operation','timestamp(ms)','latency(us)'])


threads = [1, 2, 4, 6]

op_counts= [200000, 400000, 600000] # Read
# op_counts = [20000, 40000, 60000]   # Update
# op_counts = [10000, 25000, 50000]   # Insert

# fig, ax1 = plt.subplots()
# fig, ax2 = plt.subplots()
# fig, ax4 = plt.subplots()
# fig, ax6 = plt.subplots()


for op_count in op_counts:
    # To use this script, you need to adapt csv files, so that the first row is the dataframe's header
    for thread in threads:
        results = pd.read_csv(f"/home/asc/Scrivania/NGDB/redis/workloadread/output_run_100000_{op_count}_{thread}.csv", header=0, low_memory=False)
        results.columns= ['operation','timestamp(ms)','latency(us)']
        # print(results.head(10))

        reads = results[results['operation'] == 'READ'].reset_index(drop=True).drop(columns=['operation']).astype('int32')
        scans = results[results['operation'] == 'SCAN'].reset_index(drop=True).drop(columns=['operation']).astype('int32')
        updates = results[results['operation'] == 'UPDATE'].reset_index(drop=True).drop(columns=['operation']).astype('int32')


        reads.sort_values(by=['timestamp(ms)'],ignore_index=True)
        reads['timestamp(ms)'] = reads['timestamp(ms)'] - reads.loc[0,'timestamp(ms)']

        scans.sort_values(by=['timestamp(ms)'],ignore_index=True)
        scans['timestamp(ms)'] = scans['timestamp(ms)'] - scans.loc[0,'timestamp(ms)']

        updates.sort_values(by=['timestamp(ms)'],ignore_index=True)
        updates['timestamp(ms)'] = updates['timestamp(ms)'] - updates.loc[0,'timestamp(ms)']

        reads_fast = reads[reads['latency(us)'] < 1000]
        reads_normal = reads[reads['latency(us)'] > 1000]
        reads_normal= reads_normal[reads_normal['latency(us)'] < 10000]
        reads_slow = reads[reads['latency(us)'] > 10000]

        scans_fast = scans[scans['latency(us)'] < 1000]
        scans_normal = scans[scans['latency(us)'] > 1000]
        scans_normal = scans_normal[scans_normal['latency(us)'] < 10000]
        scans_slow = scans[scans['latency(us)'] > 10000]

        updates_fast = updates[updates['latency(us)'] < 1000]
        updates_normal = updates[updates['latency(us)'] > 1000]
        updates_normal = updates_normal[updates_normal['latency(us)'] < 10000]
        updates_slow = updates[updates['latency(us)'] > 10000]


        if thread == 1:
            try:
                plt.figure()  # forces a new figure
                sns.histplot(data=reads_fast, x='latency(us)', stat='count', binwidth=50)
                sns.histplot(data=scans_fast, x='latency(us)', stat='count', binwidth=50)
                sns.histplot(data=updates_fast, x='latency(us)', stat='count', binwidth=50)
            except ValueError:
                print()
            finally:
                plt.legend(labels=["Reads","Scans","Updates"])
                # axes[0,0].set_xlim(50, 300)
                plt.title(f"100000_{op_count}_{thread}")
        elif thread == 2:
            try:
                plt.figure()  # forces a new figure
                sns.histplot(data=reads_fast, x='latency(us)', stat='count', binwidth=50)
                sns.histplot(data=scans_fast, x='latency(us)', stat='count', binwidth=50)
                sns.histplot(data=updates_fast, x='latency(us)', stat='count', binwidth=50)
            except ValueError:
                print()
            finally:
                plt.legend(labels=["Reads","Scans","Updates"])
                # axes[0,1].set_xlim(50, 300)
                plt.title(f"100000_{op_count}_{thread}")
        elif thread == 4:
            try:
                plt.figure()  # forces a new figure
                sns.histplot(data=reads_fast, x='latency(us)', stat='count', binwidth=50)
                sns.histplot(data=scans_fast, x='latency(us)', stat='count', binwidth=50)
                sns.histplot(data=updates_fast, x='latency(us)', stat='count', binwidth=50)
            except ValueError:
                print()
            finally:
                plt.legend(labels=["Reads","Scans","Updates"])
                # axes[1,0].set_xlim(50, 300)
                plt.title(f"100000_{op_count}_{thread}")
        elif thread == 6:
            try:
                plt.figure()  # forces a new figure
                sns.histplot(data=reads_fast, x='latency(us)', stat='count', binwidth=50)
                sns.histplot(data=scans_fast, x='latency(us)', stat='count', binwidth=50)
                sns.histplot(data=updates_fast, x='latency(us)', stat='count', binwidth=50)
            except ValueError:
                print()
            finally:
                plt.legend(labels=["Reads","Scans","Updates"])
                # axes[1,1].set_xlim(50, 300)
                plt.title(f"100000_{op_count}_{thread}")
    
plt.show()
    

print(reads)
print(scans)
print(updates)
