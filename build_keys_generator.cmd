rm -r ./build_key/*
rm -r ./dist_key/*
pyinstaller ./keys_generator.spec --distpath=./dist_key  --workpath=./build_key