#!/bin/bash

while read line; do echo "-->myRunall.sh: cleaning $line" && make clean_all DESIGN_CONFIG=$line; done < myStuff/designsToRun.txt

#make clean_all

while read line; do echo "-->myRunall.sh: loading $line" && make DESIGN_CONFIG=$line && make getFeatures DESIGN_CONFIG=$line && make my_gui DESIGN_CONFIG=$line; done < myStuff/designsToRun.txt #&& python3 myStuff/gateToHeat.py $DESIGN_NAME > myStuff/Python.out; done < myStuff/designsToRun.txt

printf "\n\n>>>>Done with OpenROAD runs!\n\n"



# warpping up data provided by yosys and openroad for python input
command="./gatetoheat > myStuff/gateToHeatCPP.log"
printf "\n######\n$command\n######\n\n"
eval $command



# performing training 
#command="cd myStuff && python3 regression.py > regression.log"
#printf "\n######\n$command\n######\n\n"
#eval $command


printf "\nmyRunall.sh: finished!\n"
