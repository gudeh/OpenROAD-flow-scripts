# create a folder for each file.v in this folder. 
# copy and paste 4 configuration files to folders and replace a string inside each configuration file
for x in *.v; do
  mkdir "${x%.*}" 
  
  printf "${x}\n"
#  cp "$x" "${x%.*}" # use this first for designs/src, the rest goes on designs/nangate45/
  cp constraint.sdc "${x%.*}"
  cp config.mk "${x%.*}"
  cp rules-base.json "${x%.*}"
  cp metadata-base-ok.json "${x%.*}"
  
  sed -i "s@c17@${x%.*}@" "${x%.*}/constraint.sdc"
  sed -i "s@c17@${x%.*}@" "${x%.*}/config.mk"
done


