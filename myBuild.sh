git submodule foreach git pull origin master
./build_openroad.sh --local #--latest --no_init


if [[ $1 == "run" ]]; then
	cd flow && ./myRunAll.sh &&
	printf "myBuild.sh--> Finished run!\n"
else
	printf "myBuild.sh--> Only build, no run!\n"
fi
