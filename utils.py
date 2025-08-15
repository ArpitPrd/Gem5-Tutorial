import csv

def produce_dir_names(cpu_types:list[str], cpu_freqs:list[str], mem_types:list[str]) -> list[str]:
    """
    produces the names of all the directories that store output file from the binary
    """
    dirs = []
    for cpu_type in cpu_types:
        for cpu_freq in cpu_freqs:
            for mem_type in mem_types:
                path = f"{cpu_type}_{cpu_freq}_{mem_type}_out"
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
    
    return (ipc, sim_seconds)

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
    cpu_type, cpu_freq, mem_type, _ = tuple(path.split("/")[0].split("_"))
    ipc, sim_seconds = get_stats(path)
    return [cpu_type, cpu_freq, mem_type, ipc, sim_seconds]

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

def main_save():
    cpu_types = ["O3", "TIMING", "ATOMIC"]
    cpu_freqs = ["600MHz", "800MHz", "1000MHz", "1200MHz", "1400MHz", "1600MHz", "1800MHz", "2000MHz", "2200MHz", "2400MHz", "2600MHz", "2800MHz", "3000MHz", "3200MHz", "3300MHz"]
    mem_types = ["DDR3", "DDR4", "HBM"]

    dirs = produce_dir_names(cpu_types, cpu_freqs, mem_types)

    results = get_results_from_dirs(dirs)
    field_names = ["cpu_type","cpu_freq","mem_type","ipc","sim_seconds"]
    save(results, field_names, "results.csv", "a")

if __name__ == "__main__":
    main_save()