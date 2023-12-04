from extract import extract
import csv
import numpy as np
import json

def getFieldsValuebyKey(key, data):
  print("getFieldsValuebyKey")
  print(key)
  for field in data['fields']:
    if field["field_name"] == key:
      if not field["field_value"]:
        return ''
      else:
        return field["field_value"]

def getFieldbyLanguage(maschProperty, maschData, Language, check = None):
  field = getFieldsValuebyKey(maschProperty, maschData)
  if field:
      if field[Language]:
        fieldValue = field[Language]
        return fieldValue
      else:
        return None
  else:
    return None
  
def arrayToCsv(array, filepath):
    with open(filepath, 'w', newline="\n") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerows(array)

def __main__():
  print("STARTING")
  print("EXTRACTING")
  extractData = extract()
  
  print("TRANSFORMING")
  featureList = []
  for item in extractData['records']:
    print(item['record_id'])
    print(item['record_name'])
    features =  getFieldbyLanguage('metaserver_hotel_features', item, 'de')
    print(features)
    print(type(features))
    if features:
        #featureList = np.concatenate((featureList, features), axis=None)
        #featureList = [*featureList, *features]
        featureList = list(set(featureList + features))


  print("LOADING")
  print(featureList)
  print(type(featureList))
  newList = sorted(featureList)
  arrayToCsv(featureList, "../examples/features.csv")
  #np.savetxt("../examples/features.csv", featureList)

  with open('../examples/features.json', 'w') as f:
    json.dump(newList, f, indent=4)

  print("DONE")

if __name__== "__main__":
    __main__()