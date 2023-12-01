import os
import re

def extract_elapsed_time(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        match = re.search(r'Elapsed time: (\d+:\d{1,2}(:\d{1,2})?\.\d{2})', content)
        if match:
            return match.group(1)
        else:
            return None

def convert_to_seconds(elapsed_time):
    parts = elapsed_time.split(':')
    hours = int(parts[0])
    minutes, seconds = map(float, parts[1].split('.'))
    if len(parts) == 3:
        seconds += int(parts[2])
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def process_log_files(folder_path):
    elapsed_times = {}
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    for file_name in files:
        if file_name[0].isdigit() and file_name.endswith(".log"):
            file_path = os.path.join(folder_path, file_name)
            elapsed_time = extract_elapsed_time(file_path)
            if elapsed_time:
                elapsed_times[file_name] = elapsed_time
    
    return elapsed_times

def sum_elapsed_times(elapsed_times):
    total_seconds = 0
    for elapsed_time in elapsed_times.values():
        total_seconds += convert_to_seconds(elapsed_time)
    return total_seconds

def process_folders(root_folder='./'):
    for root, dirs, files in os.walk(root_folder):
        rel_path = os.path.relpath(root, root_folder)
        
        if os.path.basename(rel_path) == 'base':
            print(f"\nProcessing folder: {root}")
            result = process_log_files(root)

            # Sort the result dictionary items by file_name
            sorted_results = sorted(result.items(), key=lambda x: x[0])

            for file_name, elapsed_time in sorted_results:
                print(f"{file_name}: Elapsed Time - {elapsed_time}")

            total_seconds = sum_elapsed_times(result)
            total_hours = total_seconds // 3600
            total_minutes = (total_seconds % 3600) // 60
            total_seconds_remainder = total_seconds % 60

            print(f"Total Elapsed Time: {int(total_hours)}:{int(total_minutes):02d}.{total_seconds_remainder:.2f}")

root_folder = './logs/asap7/'
process_folders(root_folder)
