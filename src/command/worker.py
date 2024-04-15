# Update to MASCH
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
    transformDataMASCH= transformAkeneotoMasch(productList)
  
    print("LOADING to MASCH")
    loadData = loadObjectstoMasch(transformDataMASCH)
    print("DONE")

if __name__== "__main__":
    __main__()