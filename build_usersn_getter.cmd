rm -r ./build_usersn/*
rm -r ./dist_usersn/*
pyinstaller ./usersn_getter.spec --distpath=./dist_usersn  --workpath=./build_usersn