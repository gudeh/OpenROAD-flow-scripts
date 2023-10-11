import os
import csv
import re

problems = 0
libsNotFound = []
csvsNotFound = []
cellNotFound = 0
designs_to_run_file = "./congestionPrediction/designsToRun.txt"

def extract_logic_function(line):
    # Use regular expression to extract the logic function between parentheses
    match = re.search(r'function\s*:\s*\((.*?)\)', line)
    if match:
        return match.group(1)
    else:
        return None

with open(designs_to_run_file, 'r') as designs_file:
    design_name     = ""
    design_nickName = ""
    for line in designs_file:
        line = line.strip()
        parts = line.split('/')
        print("\n------------------------------------------------------\nOuter loop with designToRun:", line, "\n------------------------------------------------------\n")
        with open(line, 'r') as makefile:
            for myline in makefile:
                if myline.strip().startswith("export DESIGN_NAME"):
                    design_name = myline.strip().split('=')[1].strip()
                if myline.strip().startswith("export DESIGN_NICKNAME"):
                    design_nickName = myline.strip().split('=')[1].strip()
        liberty_dir_path = line.replace('./designs/', './objects/').rsplit('/', 1)[0] + '/base/lib/'
        substrings_to_replace = ["black_parrot", "bp_be_top", "bp_fe_top", "bp_multi_top"]
        for substring in substrings_to_replace:
            if substring in liberty_dir_path:
                liberty_dir_path = liberty_dir_path.replace(substring, design_nickName)
        print("liberty_dir_path:", liberty_dir_path)

        cell_data_dict = {}
        try:
            liberty_file_path = os.path.join(liberty_dir_path, "merged.lib")
            if not os.path.isfile(liberty_file_path):
                files_in_dir = os.listdir(liberty_dir_path)
                if files_in_dir:
                    # Merge contents of all .lib files in the directory into merged.lib
                    with open(liberty_file_path, 'w') as merged_lib:
                        for file_name in files_in_dir:
                            if file_name.endswith('.lib'):
                                file_path = os.path.join(liberty_dir_path, file_name)
                                with open(file_path, 'r') as lib_file:
                                    merged_lib.write(lib_file.read())
                    print(f"Merged library files into {liberty_file_path}")
                else:
                    problems += 1
                    print(f"\n####################################\nNo library files found in {liberty_dir_path}\n####################################\n")
        except FileNotFoundError:
            libsNotFound.append(liberty_dir_path)
            print(f"\n####################################\nDirectory not found: {liberty_dir_path}\n####################################\n")
            continue

        if os.path.isfile(liberty_file_path):
            with open(liberty_file_path, 'r') as liberty_file:
                print( f"\n### Reading Liberty file: {liberty_file_path}" )
                liberty_data = liberty_file.read()
                lines = liberty_data.split('\n')
                cell_type = None
                area = 0.0
                input_pins = 0
                output_pins = 0
                cell_level = 0
                pin_level  = 0
                logic_function = None

                for line2 in lines:
                    line2_stripped = line2.strip()
                    # print( "line:", line2_stripped )                    
                    cell_match = re.search(r'^cell\s*\(\s*(.*?)\s*\)', line2_stripped)
                    if cell_match:
                        cell_type = cell_match.group(1)
                        match = re.search(r'cell\s*\(\s*(.*?)\s*\)', line2)
                        if match:
                            cell_type = match.group(1)
                            #print("cell_type:", cell_type)
                            cell_data_dict[cell_type] = {
                                'area': 0.0,
                                'input_pins': 0,
                                'output_pins': 0,
                                'logic_function': [] 
                            }
                        cell_level = 1
                    elif cell_type:
                        area_match = re.search(r'area\s*:\s*(\d+(\.\d+)?)', line2)
                        if area_match:
                            area = float(area_match.group(1))
                            cell_data_dict[cell_type]['area'] = area

                        if pin_level >= 1:
                            if "direction:input" in line2_stripped.replace(" ", "").replace("\t", ""):
                                cell_data_dict[cell_type]['input_pins'] += 1
                            elif "direction:output" in line2_stripped.replace(" ", "").replace("\t", ""):
                                cell_data_dict[cell_type]['output_pins'] += 1
                            logic_function_match = re.search(r'^\s*function\s*:\s*\"(.*?)\"', line2)
                            if logic_function_match:
                                # print("LF MATCH!")
                                logic_function = logic_function_match.group(1)
                                cell_data_dict[cell_type]['logic_function'].append(logic_function)

                            if "{" in line2_stripped:
                                pin_level += 1
                            elif "}" in line2_stripped:
                                pin_level -= 1
                        
                        if line2_stripped.startswith("pin"):
                            pin_level = 1
                                
                        if "{" in line2_stripped:
                            cell_level += 1
                        elif "}" in line2_stripped:
                            cell_level -= 1
                        # print( "pin level:", pin_level )
                    if cell_level == 0 and "}" in line2_stripped:
                        cell_type = None
                        area = 0.0
                        input_pins = 0
                        output_pins = 0
                        cell_level = 0
                        pin_level = 0

        # Print the dictionary before reading the CSV file for the current design
        print(f"Dictionary for {design_name}:")
        print(len(cell_data_dict))
        if len(cell_data_dict) <= 0:
            problems += 1
            print("\n####################################\nLength of Dict is <= 0\n####################################\n")


        csv_file_path = os.path.join("congestionPrediction", "dataSet", design_name, "gatesToHeat.csv")
        print(">Trying to read input csv:", csv_file_path)
        if os.path.isfile(csv_file_path):
            updated_rows = []
            with open(csv_file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                fieldnames = reader.fieldnames + ['area', 'input_pins', 'output_pins', 'logic_function']
                for row in reader:
                    logic_gate_type = row['type']
                    logic_gate_type = logic_gate_type.lstrip('\\')
                    if logic_gate_type in cell_data_dict:
                        cell_data = cell_data_dict[logic_gate_type]
                        area = cell_data['area']
                        input_pins = cell_data['input_pins']
                        output_pins = cell_data['output_pins']
                        logic_function = cell_data['logic_function']
                    else:
                        if( ("tapcell" not in logic_gate_type) and ("TAPCELL" not in logic_gate_type) \
                            and ("decap" not in logic_gate_type) and ("DECAP" not in logic_gate_type) \
                            and ("filler" not in logic_gate_type) and ("FILLER" not in logic_gate_type)):
                            cellNotFound += 1
                            print( "\n###################\nCell type not found:", logic_gate_type, "\n###################\n" )
                        area = 0.0
                        input_pins = 0
                        output_pins = 0
                        logic_function = []

                    row['area'] = area
                    row['input_pins'] = input_pins
                    row['output_pins'] = output_pins
                    row['logic_function'] = '; '.join(logic_function)  # Join logic functions into a comma-separated string
                    updated_rows.append(row)

            new_csv_file_path = os.path.join(os.path.dirname(csv_file_path), "gatesToHeatSTDfeatures.csv")
            with open(new_csv_file_path, 'w', newline='') as new_csv_file:
                writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_rows)

            print(f"New CSV file for {design_name} created successfully.")
        else:
            csvsNotFound.append( design_name )
            print(f"\n####################################\nOriginal CSV file for {design_name} not found.\n####################################\n")

print("\n\nProblems detected:", problems)
print("Cells not found:", cellNotFound)
print("Libary not found:", len( libsNotFound))
print("Library names:")
for element in libsNotFound:
    print( "\t", element)
print("CSVs not found:", len( csvsNotFound ) )
for element in csvsNotFound:
    print( "\t", element )
