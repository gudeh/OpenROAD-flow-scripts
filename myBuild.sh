git submodule foreach git pull origin master
./build_openroad.sh --local --latest --no_init

#if [$1 == "run"]
#	then cd flow && ./myRunAll.sh
#fi
