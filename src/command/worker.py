# Update to MASCH
import json
import sys
sys.path.append("..")

from service.objectStorage import getObject, getObjects, putObject, countFilesInFolder, folderExist
from service.masch import getMaschUpdateJobs, checkProductsMasch, transformAkeneotoMasch, loadObjectstoMasch

def __main__():
    print("STARTING - WORKER")
    print("GET MASCH UPDATES")
    updateList = getMaschUpdateJobs()
    print(updateList)
    productList = getObjects(updateList)

    print("TRANSFORMING from Akeneo to MASCH")
    #print (productList)
    transformDataMASCH = transformAkeneotoMasch(productList)

    # Add transformDataMASCH to json file in output folder
    print("WRITING to output/transformDataMasch.json")
    with open("../../output/transformDataMasch.json", "w") as file:
        file.write(json.dumps(transformDataMASCH, indent=4))
  
    print("LOADING to MASCH")
    loadData = loadObjectstoMasch(transformDataMASCH)

    print ("CLEAR MASCH UPDATE LIST")
    updateList = {}
    putObject(updateList, 'export/contentdesk/job/masch/updates/index.json')
    print("DONE")

if __name__== "__main__":
    __main__()