#run ./script.sh inputfolder BR Rfactor(luminocity ratio)
for f in "$1"/*.dat; do
    python parameter_scan.py "$f" "$2" "$3"
done
