#!/usr/bin/env python3
import json,csv,sys,re,datetime,hashlib
from sys import argv
import numpy as np

if len(argv)<3:
  sys.exit(f"Usage {argv[0]} input.json output.csv")

# read CSV file containing filenames of scans and previously generated file IDs
filenames = {}
links = {}
with open("IDs/alleIDs.csv") as f:
  reader = csv.DictReader(f, fieldnames=["uuid","name","width","height","link"])
  for row in reader:
    filenames[row["uuid"]] = row["name"]
    links[row["uuid"]] = row["link"]

def getDateISO(date):
  try:
    return datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
  except ValueError:
    return ""

# read results from HetVolk.org
with open(argv[1]) as f:
  items = []
  data = json.load(f)
  outputheader = [ 
    "id", "filename", # from record
    "link", # from record>LUT
    "type", # type of antwoord

    "title", "fname", "prefix", "sname", "bdate", "bdate-iso", "bplace", "crime", "street", "housenr", "housenr_postfix", "place", "ddate", "ddate-iso", "date_departure", "date_departure-iso", "prolong", "date_arrival", "date_arrival-iso", # from person or biljetten

    "place", "street", "housenr", "date_ingebruik", "date_vrij", "o_fname", "o_prefix", "o_sname", "o_place", "o_street", "o_housenr", "o_housenr_postfix", "date_ingebruik-iso", "date_vrij-iso", "r_place", "r_fname", "r_prefix", "r_street", "r_housenr", "r_housenr_postfix", "r_sname", # from Parcel (gevorderde percelen)

    "user", "tijdstip"] # from antwoord

  outputheader = np.unique(outputheader)  # make unique using numpy. there should be another way

  output = csv.DictWriter(open(argv[2],'w',encoding='utf-8-sig'), fieldnames=outputheader, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
  output.writeheader()

  for record in data:
    record["filename"] = filenames[record["id"]]  #get filename from lookup table
    record["link"] = links[record["id"]] #"=HYPERLINK(\"{}\")".format(links[record["id"]])  #get filename from lookup table
    record["tijdstip"] = record["tijdstip"]

    if not "antwoord" in record:  # geen antwoorden dus voeg record as-is toe als item
      output.writerow(record)

    elif isinstance(record["antwoord"], dict):
      
      for itemType in record["antwoord"].keys(): # dataType
        items = record["antwoord"][itemType]
        
        for item in items:
          if not isinstance(item, dict): # for example: "last": "Rijksen"
            continue

          print(item)
          item["type"] = itemType
          for itemKey in list(item): # makes a copy of item for itemKey iteration only (prevent dictionary changed size during iteration)
            if itemKey.find("date")>-1:
              item[itemKey+"-iso"] = getDateISO(item[itemKey])   # modify original
         
          item.update(record)  # merge record values with person
          del(item["antwoord"]) # remove antwoord value since we have those values in person
          output.writerow(item)


      # if "person" in record["antwoord"]
      #   or "biljetten" in record["antwoord"]: # een of meerdere antwoorden dus voeg elk antwoord toe als afzonderlijk item
        

      #   for item in record["antwoord"]["person"]:
      #     item["type"]="person" # set type in case we will have other items than just person
          
         
      # if "biljetten" in record["antwoord"]: # een of meerdere antwoorden dus voeg elk antwoord toe als afzonderlijk item
      #   for item in record["antwoord"]["person"]:
      #     item["type"]="person" # set type in case we will have other items than just person
          
      #     if "bdate" in item:
      #       item["bdate-iso"]=getDateISO(item["bdate"])
          
      #     if "ddate" in item:
      #       item["ddate-iso"]=getDateISO(item["ddate"])

      #     item.update(record)  # merge record values with person
      #     del(item["antwoord"]) # remove antwoord value since we have those values in person
      #     output.writerow(item)

    
