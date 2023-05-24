from os import getenv
from urllib.parse import urlparse
from dotenv import find_dotenv, load_dotenv
from akeneo.akeneo import Akeneo
import requests
import os
load_dotenv(find_dotenv())

AKENEO_HOST = getenv('AKENEO_HOST')
AKENEO_CLIENT_ID = getenv('AKENEO_CLIENT_ID')
AKENEO_CLIENT_SECRET = getenv('AKENEO_CLIENT_SECRET')
AKENEO_USERNAME = getenv('AKENEO_USERNAME')
AKENEO_PASSWORD = getenv('AKENEO_PASSWORD')

MASCH_URL = getenv('MASCH_URL')
MASCH_PULL_URL = getenv('MASCH_PULL_URL')
MASCH_USER = getenv('MASCH_USER')
MASCH_PASSWORD = getenv('MASCH_PASSWORD')

def load(data):
  akeneo = Akeneo(
    AKENEO_HOST,
    AKENEO_CLIENT_ID,
    AKENEO_CLIENT_SECRET,
    AKENEO_USERNAME,
    AKENEO_PASSWORD
  )
  for item in data:
    print(item)
    akeneo.patchProductByCode(item['identifier'], item)
    #akeneo.patchProducts(item)

def loadImages(data):
  akeneo = Akeneo(
    AKENEO_HOST,
    AKENEO_CLIENT_ID,
    AKENEO_CLIENT_SECRET,
    AKENEO_USERNAME,
    AKENEO_PASSWORD
  )
  for item in data:
    print(item)
    akeneo.postMediaFileProduct(item['filePath'], item['identifier'], item['attribute'], item['locale'], item['scope'])

def downloadImages(data):
  print("Remove Folders")
  removeAllFilesinFolder('downloads')
  print("Download Images")
  for item in data:
    print(item)
    if not item['filePath']:
      imagePath = urlparse(item['filePath'])
      filename = os.path.basename(imagePath.path)
      print(filename)
      r = requests.get(item['filePath'], allow_redirects=True)
      PATH = '/downloads/'+item['identifier']+'/'
      if not os.path.exists(PATH):
        os.makedirs(PATH)
      open(PATH+filename, 'wb').write(r.content)

def removeAllFilesinFolder(folder):
  filelist = [ f for f in os.listdir(folder) ]
  for f in filelist:
    os.remove(os.path.join(folder, f))