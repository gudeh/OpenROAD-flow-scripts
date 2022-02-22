#!/bin/bash
make clean_all

while read line; do echo "loading $line" && make DESIGN_CONFIG=$line && make my_gui DESIGN_CONFIG=$line; done < myStuff/designsToRun.txt

printf "---->Done with OpenROAD runs!\n---->Executing Python to handle all CSVs!\n"
python3 myStuff/gateToHeat.py > myStuff/Python.out
