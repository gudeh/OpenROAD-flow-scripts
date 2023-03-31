#!/bin/bash

#while read line; do 
#  echo "-->myRunall.sh: cleaning $line" #&& 
#  make clean_all DESIGN_CONFIG=$line; 
#done < congestionPrediction/designsToRun.txt

#make clean_all

set doClean false
set doRun false

while read line; do 

    if [ "$doClean" = true ] ; then
        echo "-->myRunall.sh: cleaning $line" #&& 
        make clean_all DESIGN_CONFIG=$line; 
    fi
  
    if [ "$doRun" = true ] ; then
        echo "-->myRunall.sh: loading $line" #&&
        make DESIGN_CONFIG=$line #&& 
    fi
    
    make getFeatures DESIGN_CONFIG=$line #&& 
    make my_gui DESIGN_CONFIG=$line; 
    #  make gui_final DESIGN_CONFIG=$line; 
    
done < congestionPrediction/designsToRun.txt 

printf "\n\n>>>>Done with OpenROAD runs!\n\n"



# wrapping up data provided by yosys and openroad for python input
command="./gateToHeat > congestionPrediction/gateToHeatCPP.log"
printf "\n######\n$command\n######\n\n"
eval $command



# performing training 
#command="cd congestionPrediction && python3 regression.py > regression.log"
#printf "\n######\n$command\n######\n\n"
#eval $command


printf "\nmyRunall.sh: finished!\n"
