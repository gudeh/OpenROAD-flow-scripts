#!/bin/bash

doMyCleanAll=true
doORCleanIter=true
doRun=true

#TODO fix rm of dataSet
if [ "$doMyClean" = true ] ; then
    echo "--> rm -rf congestionPrediction/dataSet/*"
    rm -rf congestionPrediction/dataSet/*
    echo "--> rm -rf congestionPrediction/layoutPrints/*"
    rm -rf congestionPrediction/layoutPrints/*
fi


while read line; do 
   
    if [ "$doORCleanIter" = true ] ; then
        echo "--> myRunall.sh: cleaning $line" #&& 
        make clean_all DESIGN_CONFIG=$line;
    fi
  
    if [ "$doRun" = true ] ; then
        echo "--> myRunall.sh: loading $line" #&&
        make DESIGN_CONFIG=$line #PLACE_DENSITY=0.95 #PLACE_DENSITY_LB_ADDON= #&& 
    fi

    #TODO rename my_gui to getLabel
    make getFeatures DESIGN_CONFIG=$line #&& 
    make my_gui DESIGN_CONFIG=$line
    #  make gui_final DESIGN_CONFIG=$line; 
    
done < congestionPrediction/designsToRun.txt 

printf "\n\n>>>>Done with OpenROAD runs!\n\n"



# wrapping up data provided by yosys and openroad for python input
command="./gateToHeat > congestionPrediction/gateToHeatCPP.log"
printf "\n######\n$command\n######\n\n"
eval $command

command="python3 getBasicFeatures.py > congestionPrediction/getBasicFeatures.log"
printf "\n######\n$command\n######\n\n"
eval $command

# performing training 
#command="cd congestionPrediction && python3 regression.py > regression.log"
#printf "\n######\n$command\n######\n\n"
#eval $command

printf "\nmyRunall.sh: finished!\n"
