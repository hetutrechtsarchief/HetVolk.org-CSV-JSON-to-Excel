<?php
$rows = [];

if (($file = fopen($argv[1], "r")) !== FALSE) {
  if (fgets($file, 4) !== "\xef\xbb\xbf") rewind($file); //Skip BOM if present

  while (($data = fgetcsv($file, 0, ";", "\"" , "\\")) !== FALSE) {
    if ($data[0]=="itemID") continue; # skip first row
    $row = [];
    $row["id"] = $data[0];
    $row["title"] = $data[1];
    $row["antwoord"] = json_decode($data[2]);
    $row["user"] = $data[3];
    $row["tijdstip"] = $data[4];
    $rows[] = $row; # skip first row
  }
  fclose($file);
}

echo(json_encode($rows,JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
?>