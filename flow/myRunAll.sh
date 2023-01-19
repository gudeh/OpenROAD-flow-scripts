#!/bin/bash

while read line; do echo "-->myRunall.sh: cleaning $line" && make clean_all DESIGN_CONFIG=$line; done < myStuff/designsToRun.txt

#make clean_all

while read line; do echo "-->myRunall.sh: loading $line" && make DESIGN_CONFIG=$line && make getFeatures DESIGN_CONFIG=$line && make my_gui DESIGN_CONFIG=$line; done < myStuff/designsToRun.txt #&& python3 myStuff/gateToHeat.py $DESIGN_NAME > myStuff/Python.out; done < myStuff/designsToRun.txt

printf ">>>>Done with OpenROAD runs!\n>>>>Handling all CSVs!\n"
#printf "design config $DESIGN_CONFIG\n"
#printf "platform $PLATFORM\n"
#python3 myStuff/gateToHeat.py > myStuff/Python.out
./gatetoheat > myStuff/gateToHeatCPP.log # warpping up data provided by yosys and openroad for python input
python3 myStuff/regression.py > myStuff/regression.log # performing training 
printf "myRunall.sh: finished!\n"
