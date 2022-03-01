#!/bin/bash

while read line; do echo "-->myRunall.sh: cleaning $line" && make clean_all DESIGN_CONFIG=$line; done < myStuff/designsToRun.txt

#make clean_all

while read line; do echo "-->myRunall.sh: loading $line" && make DESIGN_CONFIG=$line && make getFeatures DESIGN_CONFIG=$line && make my_gui DESIGN_CONFIG=$line; done < myStuff/designsToRun.txt

printf ">>>>Done with OpenROAD runs!\n>>>Executing Python to handle all CSVs!\n"
python3 myStuff/gateToHeat.py > myStuff/Python.out
printf "myRunall.sh: finished!\n"
