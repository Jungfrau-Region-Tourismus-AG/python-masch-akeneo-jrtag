from extract import extract, getAkeneoProducts
from transform import transform, transformAkeneotoMasch
from load import load

def __main__():
  print("STARTING")
  print("EXTRACTING")
  extractData = extract()
  extractDataAkeneo = getAkeneoProducts()
  
  print("TRANSFORMING")
  transformDataAkeneo = transformAkeneotoMasch(extractDataAkeneo)
  transformData = transform(extractData, transformDataAkeneo)
  
  print(transformDataAkeneo[16042])
  #transformData2 = transfromToAkeneo(transformData)
  print(transformData)
  
  print("LOADING")
  loadData = load(transformData)
  print("DONE")

if __name__== "__main__":
    __main__()