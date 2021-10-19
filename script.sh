
while [[ "$1" != "" ]] ; do   ## for filepath in csv-input/*.csv; do
  filepath=$1
  filename=${filepath##*/}
  basename="${filename%.*}"

  echo $basename
  php index.php "$filepath" > "json/$basename.json"
  ./flatten.py "json/$basename.json" "csv-output/$basename.csv"
  ./csv2xlsx_osx --colsep , --overwrite --infile "csv-output/$basename.csv" --outfile "xlsx-output/$basename.xlsx"
  echo 

  shift
done

