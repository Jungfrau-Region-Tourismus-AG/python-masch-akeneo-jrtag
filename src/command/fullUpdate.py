
import datetime
import sys
sys.path.append("..")

from service.extract import extract, getAkeneoProducts
from service.transform import transform, transformAkeneotoMasch, createHashAkeneo, createHashMASCH
from service.load import load
import json
import service.debug as debug
#import service.objectStorage as objectStorage

def __main__():
  print("STARTING")
  print("EXTRACTING")
  extractData = extract()
  extractDataAkeneo = getAkeneoProducts()
  
  debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "extractDataAkeneo", extractDataAkeneo)
  
  #hashAkeneo = createHashAkeneo(extractDataAkeneo)
  #hashMasch = createHashMASCH(extractDataAkeneo)
  # Convert hashMasch to JSON
  #hashMasch_json = json.dumps(hashMasch, indent=4)
  #debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "hashMasch", hashMasch_json)
  
  print("   - Backup to Object Storage")
  current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
  str_current_datetime = str(current_datetime)
  #objectStorage.exportProduct(extractDataAkeneo, 'export/contentdesk/fullUpdate/'+str_current_datetime, "contentdeskExport")
  
  print("TRANSFORMING")
  #transformAkeneotoMaschData = transformAkeneotoMasch(extractDataAkeneo)
  #debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "transformDataAkeneo", transformAkeneotoMaschData)
  transformData = transform(extractData, extractDataAkeneo)
  debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "transformData", transformData)
  
  print("LOADING")
  loadData = load(transformData)
  debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "loadData", loadData)
  print("DONE")

if __name__== "__main__":
    __main__()