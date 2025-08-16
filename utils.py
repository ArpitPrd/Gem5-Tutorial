import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def produce_dir_names(cpu_types:list[str], cpu_freqs:list[str], mem_types:list[str]) -> list[str]:
    """
    produces the names of all the directories that store output file from the binary
    """
    dirs = []
    for cpu_type in cpu_types:
        for cpu_freq in cpu_freqs:
            for mem_type in mem_types:
                path = f"out100/{cpu_type}_{cpu_freq}_{mem_type}_out"
                dirs.append(path)

    return dirs

def _get_stats(filename: str) -> dict:
    """
    Reads gem5 stats.txt and returns {stat_name: float_value}.
    Skips histogram table rows that don't follow the key-value format.
    """
    stats = {}
    f = open(filename, 'r')
    lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue

        parts = line.split()
        # normal stat lines have: key, value, "#", comment...
        if len(parts) >= 2 and parts[1].replace('.', '', 1).replace(',', '').isdigit():
            key = parts[0]
            val = float(parts[1].replace(",", ""))
            stats[key] = val
    f.close()
    return stats

def compile_stats(stats:dict) -> tuple:
    """
    extracts ueful information
    as of now extracts only ipc, sim_seconds
    """
    ipc = stats.get("board.processor.cores.core.ipc", 0)
    sim_seconds = stats.get("simSeconds", 0)
    read_avg_lat = stats.get("board.memory.mem_ctrl.requestorReadAvgLat::cache_hierarchy.ruby_system.directory_controllers", 0)
    write_avg_lat = stats.get("board.memory.mem_ctrl.requestorWriteAvgLat::cache_hierarchy.ruby_system.directory_controllers", 0)
    return [ipc, sim_seconds, read_avg_lat, write_avg_lat]

def get_stats(filename:str) -> tuple:
    """
    wrapper to get and compile
    """
    stats = _get_stats(filename)
    return compile_stats(stats)

def get_results_from_stats(path:str) -> list:
    """
    wraps the reuslt for one file
    """
    cpu_type, cpu_freq, mem_type, _ = tuple(path.split("/")[1].split("_"))
    return [cpu_type, cpu_freq, mem_type] + get_stats(path)

def get_results_from_dirs(dirs):
    results = []
    for dir in dirs:
        path = dir + "/stats.txt"
        result = get_results_from_stats(path)
        results.append(result)

    return results

def save(lists_to_save:list, field_names:list, save_loc:str, mode:str):
    """
    general purpose saver
    """
    with open(save_loc, mode=mode, newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # writer.writeheader()
        for list_to_save in lists_to_save:
            dict_to_save = {}
            for i, field_name in enumerate(field_names):
                dict_to_save[field_name] = list_to_save[i]
            writer.writerow(dict_to_save)

        

    print(f"file saved @ {save_loc}")

def main_plotting(filename):

    df = pd.read_csv(filename)

    # Example: IPC vs Clock for O3
    o3_df = df[df["cpu_type"] == "O3"]
    for mem in o3_df["mem_type"].unique():
        sub = o3_df[o3_df["mem_type"] == mem]
        plt.plot(sub["cpu_freq"], sub["ipc"], label=mem)
    plt.legend()
    plt.xlabel("Clock Frequency")
    plt.ylabel("IPC")
    plt.title("O3 CPU - IPC vs Clock for Different Memory Types")
    plt.show()



def plot_ipc_vs_freq_bar(csv_path):
    """
    Reads a CSV file with CPU simulation results and generates a grouped bar plot.

    This version of the function is updated to filter the data for rows where the
    'mem_type' is specifically 'DDR3' before plotting. It then plots
    IPC (Instructions Per Cycle) on the Y-axis and CPU Frequency on the X-axis,
    with separate bars for the 'O3' and 'TIMING' CPU types.

    Args:
        csv_path (str): The file path to the results.csv file.
    """

    # Load the data from the specified CSV file
    df = pd.read_csv(csv_path)

    # Filter the DataFrame to include only 'O3' and 'TIMING' CPU types,
    # AND to fix the 'mem_type' to 'DDR3' as requested.
    # The '&' operator performs a logical AND on the two conditions.
    filtered_df = df[(df['cpu_type'].isin(['O3', 'TIMING'])) & (df['mem_type'] == 'DDR3')]

    filtered_df = filtered_df.sort_values(by='cpu_freq')

    sns.set_style("whitegrid")

    # 'x' is the independent variable (frequency).
    # 'y' is the dependent variable (IPC).
    plt.figure(figsize=(10, 6)) 
    sns.barplot(
        x='cpu_freq',
        y='ipc',
        hue='cpu_type',
        data=filtered_df,
        palette='viridis' 
    )

    plt.title('IPC vs. CPU Frequency for O3 and TIMING CPU Types (mem_type = DDR3)', fontsize=16)
    plt.xlabel('CPU Frequency (Hz)', fontsize=12)
    plt.ylabel('Instructions Per Cycle (IPC)', fontsize=12)
    plt.legend(title='CPU Type')

    for p in plt.gca().patches:
        height = p.get_height()
        plt.gca().text(p.get_x() + p.get_width() / 2, height,
                       f'{height:.2f}', ha='center', va='bottom',
                       fontsize=10, color='black')

    plt.tight_layout() 
    plt.show()

def plot_ipc_vs_freq_line(csv_path):
    """
    Reads a CSV file with CPU simulation results and generates a grouped line plot.

    This version of the function filters the data for rows where the
    'mem_type' is specifically 'DDR3'. It then plots IPC (Instructions Per Cycle)
    on the Y-axis and CPU Frequency on the X-axis, using separate lines
    for the 'O3' and 'TIMING' CPU types to show performance trends.

    Args:
        csv_path (str): The file path to the results.csv file.
    """

    df = pd.read_csv(csv_path)

    filtered_df = df[(df['cpu_type'].isin(['DDR3', 'HBM'])) & (df['cpu_type'] == 'O3')]

    filtered_df = filtered_df.sort_values(by='cpu_freq')

    sns.set_style("whitegrid")

    # 'x' is the independent variable (frequency).
    # 'y' is the dependent variable (IPC).
    plt.figure(figsize=(10, 6)) # Set a good figure size
    sns.lineplot(
        x='cpu_freq',
        y='ipc',
        hue='mem_type',
        data=filtered_df,
        marker='o',
        palette='viridis' 
    )

    plt.title('IPC vs. CPU Frequency for DDR3 and HBM CPU Types (cpu_type = O3)', fontsize=16)
    plt.xlabel('CPU Frequency (Hz)', fontsize=12)
    plt.ylabel('IPC', fontsize=12)
    plt.legend(title='Mem Type')

    plt.tight_layout() 
    plt.show()

def plot_gem5_stats(csv_path, x_axis_metric, y_axis_metric, hue_metric, fixed_filters):
    """
    A modular function to plot gem5 simulation results from a CSV file.

    The function dynamically plots any two metrics against each other while
    allowing you to filter the data based on fixed parameters.

    Args:
        csv_path (str): The file path to the results.csv file.
        x_axis_metric (str): The name of the column for the X-axis (e.g., 'cpu_freq').
        y_axis_metric (str): The name of the column for the Y-axis (e.g., 'ipc', 'sim_seconds').
        hue_metric (str): The column name to use for different lines on the plot
                          (e.g., 'cpu_type', 'mem_type').
        fixed_filters (dict): A dictionary of columns and their values to filter the
                              data (e.g., {'cpu_type': 'O3', 'mem_type': 'DDR3'}).
    """

    try:
        # Load the data from the specified CSV file
        df = pd.read_csv(csv_path)

        # Apply the fixed filters to the DataFrame
        for column, value in fixed_filters.items():
            # Check if the column exists in the DataFrame
            if column not in df.columns:
                print(f"Error: Fixed filter column '{column}' not found in CSV.")
                return
            
            # Check if the value is in the column (case-insensitive for robustness)
            if isinstance(value, str):
                df = df[df[column].str.contains(value, case=False, na=False)]
            else:
                df = df[df[column] == value]

        # Ensure the specified plotting columns exist
        if x_axis_metric not in df.columns or y_axis_metric not in df.columns or hue_metric not in df.columns:
            print(f"Error: One of the plotting columns does not exist in the data. Please check '{x_axis_metric}', '{y_axis_metric}', and '{hue_metric}'.")
            return

        if df.empty:
            print("Warning: No data found after applying filters. No plot will be generated.")
            return

        # Handle the case where the X-axis is CPU frequency with a string suffix
        if x_axis_metric == 'cpu_freq' and df[x_axis_metric].dtype == 'object':
            # Extract the numeric part and create a temporary column for sorting
            df['sort_key'] = df[x_axis_metric].str.extract('(\d+)').astype(int)
            df = df.sort_values(by='sort_key')
        else:
            # Sort the data by the specified X-axis metric
            df = df.sort_values(by=x_axis_metric)

        sns.set_style("whitegrid")

        plt.figure(figsize=(10, 6)) 
        sns.lineplot(
            x=x_axis_metric,
            y=y_axis_metric,
            hue=hue_metric,
            data=df,
            marker='o', 
            palette='viridis' 
        )

        fixed_str = ", ".join([f"{k} = {v}" for k, v in fixed_filters.items()])
        title = f"{y_axis_metric.upper()} vs. {x_axis_metric.upper()} ({fixed_str})"
        
        plt.title(title, fontsize=16)
        plt.xlabel(x_axis_metric.replace('_', ' ').title(), fontsize=12)
        plt.ylabel(y_axis_metric.replace('_', ' ').title(), fontsize=12)
        plt.legend(title=hue_metric.replace('_', ' ').title())

        plt.tight_layout() 
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

def main_save():
    cpu_types = ["O3", "TIMING"]
    cpu_freqs = ["600MHz", "800MHz", "1000MHz", "1200MHz", "1400MHz", "1600MHz", "1800MHz", "2000MHz", "2200MHz", "2400MHz", "2600MHz", "2800MHz", "3000MHz", "3200MHz", "3300MHz"]
    mem_types = ["DDR3", "HBM", "DDR4", "DualDDR3"]

    dirs = produce_dir_names(cpu_types, cpu_freqs, mem_types)

    results = get_results_from_dirs(dirs)
    field_names = ["cpu_type","cpu_freq","mem_type","ipc","sim_seconds", "read_avg_lat", "write_avg_lat"]
    save(results, field_names, "results_with_lat.csv", "a")

if __name__ == "__main__":
    main_save()
    # plot_gem5_stats("results_4_mems.csv", "cpu_freq", "sim_seconds", "mem_type", {"cpu_type":"O3"})