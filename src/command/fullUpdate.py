
import sys
sys.path.append("..")

from service.extract import extract, getAkeneoProducts
from service.transform import transform, transformAkeneotoMasch, createHashAkeneo, createHashMASCH
from service.load import load
import service.debug as debug

def __main__():
  print("STARTING")
  print("EXTRACTING")
  extractData = extract()
  extractDataAkeneo = getAkeneoProducts()
  
  debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "extractDataAkeneo", extractDataAkeneo)
  
  #hashAkeneo = createHashAkeneo(extractDataAkeneo)
  hashMasch = createHashMASCH(extractDataAkeneo)
  debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "hashMasch", hashMasch)
  
  print("TRANSFORMING")
  #transformAkeneotoMaschData = transformAkeneotoMasch(extractDataAkeneo)
  #debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "transformDataAkeneo", transformAkeneotoMaschData)
  transformData = transform(extractData, hashMasch)
  debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "transformData", transformData)
  
  print("LOADING")
  loadData = load(transformData)
  debug.addToFileFull("fullUpdate", "ziggy", "export", "maschId", "loadData", loadData)
  print("DONE")

if __name__== "__main__":
    __main__()