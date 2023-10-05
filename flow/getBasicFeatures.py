import os
import csv
import re

problems = 0

# Define the path to the file containing the list of designs to process
designs_to_run_file = "./congestionPrediction/designsToRun.txt"

# Read the lines from the file and process each design
with open(designs_to_run_file, 'r') as designs_file:
    for line in designs_file:
        # Strip leading and trailing whitespace from the line
        line = line.strip()

        # Extract the design name from the line
        parts = line.split('/')
        if len(parts) >= 4:
            design_name = parts[3]
            print("design_name:", design_name)
        else:
            problems += 1
            print(f"\n####################################\nDesign name not found in line: {line}\n####################################\n")
            # continue

        # Define the path to the directory containing liberty files for the current design
        liberty_dir_path = line.replace('./designs/', './objects/').rsplit('/', 1)[0] + '/base/lib/'
        print("liberty_dir_path:", liberty_dir_path)

        # Define a dictionary to store cell data including area, input_pins, and output_pins
        cell_data_dict = {}

        # Check if the merged.lib file is present, otherwise select the first file in the directory
        if os.path.isfile(os.path.join(liberty_dir_path, "merged.lib")):
            liberty_file_path = os.path.join(liberty_dir_path, "merged.lib")
        else:
            # Get the first file in the directory as the library file
            files_in_dir = os.listdir(liberty_dir_path)
            if files_in_dir:
                liberty_file_path = os.path.join(liberty_dir_path, files_in_dir[0])
            else:
                problems += 1
                print(f"\n####################################\nNo library files found in {liberty_dir_path}\n####################################\n")                
                # continue

        # Read the liberty file and populate the dictionary
        if os.path.isfile(liberty_file_path):
            with open(liberty_file_path, 'r') as liberty_file:
                liberty_data = liberty_file.read()
                lines = liberty_data.split('\n')
                cell_type = None
                area = 0.0
                input_pins = 0
                output_pins = 0
                cell_level = 0
                pin_level  = 0
                for line2 in lines:
                    line2_stripped = line2.strip()
                    # print("stripped:",line2_stripped)
                    #print("line2_stripped.replace(" ", ""):",line2_stripped.replace(" ", "").replace("\t", ""))
                    if line2_stripped.startswith("cell"):
                        # print("starts with cell")
                        # Use regular expression to extract the cell type between parentheses
                        match = re.search(r'cell\s*\(\s*(.*?)\s*\)', line2)
                        if match:
                            cell_type = match.group(1)
                            print("cell_type:",cell_type)
                            cell_data_dict[cell_type] = {
                                'area': 0.0,
                                'input_pins': 0,
                                'output_pins': 0
                            }
                        cell_level = 1
                    elif cell_type:
                        #print("line2_stripped.replace(" ", ""):",line2_stripped.replace(" ", "").replace("\t", ""))
                        # print("cell_level == 1")
                        area_match = re.search(r'area\s*:\s*(\d+(\.\d+)?)', line2)
                        if area_match:
                            area = float(area_match.group(1))
                            # print("AREA:",area)
                            cell_data_dict[cell_type]['area'] = area
                        if line2_stripped.startswith("pin"):
                            print("Pin true")
                            pin_level = 1
                        if  "{" in line2_stripped:
                            cell_level += 1
                        elif  "}" in line2_stripped:
                            cell_level -= 1
                        if pin_level >= 1:
                            print("pin and cell >=1")
                            #print("line2_stripped.replace(" ", ""):",line2_stripped.replace(" ", "").replace("\t", ""))
                            if "direction:input" in line2_stripped.replace(" ", "").replace("\t", ""):
                                print("TRUEEE")
                                cell_data_dict[cell_type]['input_pins'] += 1
                            elif "direction:output" in line2_stripped.replace(" ", "").replace("\t", ""):
                                cell_data_dict[cell_type]['output_pins'] += 1
                            if  "{" in line2_stripped:
                                pin_level += 1
                            elif  "}" in line2_stripped:
                                pin_level -= 1
                    if cell_level == 0 and line2_stripped == "}":
                        cell_type = None
                        area = 0.0
                        input_pins = 0
                        output_pins = 0
                        cell_level = 0
                        pin_level = 0

        # Print the dictionary before reading the CSV file for the current design
        print(f"Dictionary for {line}:")
        print(len(cell_data_dict))
        if( len(cell_data_dict) <= 0 ):
            problems += 1
            print("\n####################################\nLength of Dict is <= 0\n####################################\n")

        # Define the path to the original CSV file for the current design
        csv_file_path = os.path.join("congestionPrediction", "dataSet", design_name, "gatesToHeat.csv")
        print("input csv_file_path:", csv_file_path)

        # Check if the original CSV file exists
        if os.path.isfile(csv_file_path):
            # Create a list to store updated CSV rows
            updated_rows = []

            # Read the original CSV file
            with open(csv_file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)

                # Manually specify fieldnames based on your CSV structure
                fieldnames = reader.fieldnames + ['area', 'input_pins', 'output_pins']

                for row in reader:
                    logic_gate_type = row['type']

                    # Remove '\' from the beginning of the type if present
                    logic_gate_type = logic_gate_type.lstrip('\\')

                    # Get cell data from the dictionary if it exists
                    if logic_gate_type in cell_data_dict:
                        cell_data = cell_data_dict[logic_gate_type]
                        area = cell_data['area']
                        input_pins = cell_data['input_pins']
                        output_pins = cell_data['output_pins']
                    else:
                        area = 0.0
                        input_pins = 0
                        output_pins = 0

                    # Add the 'area', 'input_pins', and 'output_pins' columns to the row
                    row['area'] = area
                    row['input_pins'] = input_pins
                    row['output_pins'] = output_pins
                    updated_rows.append(row)

            # Define the path for the new CSV file in the same directory as the original CSV
            new_csv_file_path = os.path.join(os.path.dirname(csv_file_path), "gatesToHeatSTDfeatures.csv")

            # Write the updated rows to the new CSV file
            with open(new_csv_file_path, 'w', newline='') as new_csv_file:
                writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_rows)

            print(f"New CSV file for {design_name} created successfully.")
        else:
            problems += 1
            print(f"\n####################################\nOriginal CSV file for {design_name} not found.\n####################################\n")

print("Problems detected:", problems)
