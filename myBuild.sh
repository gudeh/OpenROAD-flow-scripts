sudo git submodule foreach git pull origin master
git checkout master
git fetch --all
git merge origin/master
git clean -xdf ./tools
./build_openroad.sh --local --latest --no_init
