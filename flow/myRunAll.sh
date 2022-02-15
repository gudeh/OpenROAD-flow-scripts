#!/bin/bash
while read line; do echo "loading $line" && make DESIGN_CONFIG=$line && make my_gui DESIGN_CONFIG=$line; done < myStuff/designsToRun.txt
