import sys
sys.path.append("..")

from service.extract import extract, getAkeneoProducts
from service.transform import transformImage, transformAkeneotoMasch
from service.load import downloadImages,loadImages


def __main__():
  print("STARTING")
  print("EXTRACTING")
  extractData = extract()
  extractDataAkeneo = getAkeneoProducts()
  
  print("TRANSFORMING")
  #transformDataAkeneo = transformAkeneotoMasch(extractDataAkeneo)
  transformImageData = transformImage(extractData, extractDataAkeneo, 'teaser_and_content_banner_picture_winter', 'image_winter')
  #transformImageDataSummer = transformImage(extractData, transformDataAkeneo, 'teaser_and_content_banner_picture_summer', 'image_summer')
  #transformImageDataWinter = transformImage(extractData, transformDataAkeneo, 'teaser_and_content_banner_picture_winter', 'image_winter')
  
  print("LOADING")
  #loadData = load(transformData)
  print("DOWNLOAD IMAGES")
  downloadFiles = downloadImages(transformImageData)
  #downloadFilesSummer = downloadImages(transformImageDataSummer)
  #downloadFilesWinter = downloadImages(transformImageDataWinter)
  print("LOAD IMAGES")
  loadData = loadImages(transformImageData)
  #loadDataSummer = loadImages(transformImageDataSummer)
  #loadDataWinter = loadImages(transformImageDataWinter)
  print("DONE")

if __name__== "__main__":
    __main__()