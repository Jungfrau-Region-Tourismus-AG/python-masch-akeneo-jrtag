from os import getenv
from urllib.parse import urlparse
from dotenv import find_dotenv, load_dotenv
from akeneo.akeneo import Akeneo
import requests
import os, shutil
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
    print(item['identifier']+': '+item['values']['maschId'][0]['data'])
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
    print(item['identifier'])
    dir_path = os.path.dirname(os.path.realpath(__file__))
    PATH = dir_path+'/downloads/'+item['identifier']+'/'+item['filename']
    akeneo.postMediaFileProduct(PATH, item['identifier'], item['attribute'], item['locale'], item['scope'])

def downloadImages(data):
  print("Remove Folders")
  removeAllFilesinFolder('downloads')
  print("Download Images")
  for item in data:
    if item['filePath']:
      imagePath = urlparse(item['filePath'])
      filename = os.path.basename(imagePath.path)
      dir_path = os.path.dirname(os.path.realpath(__file__))
      r = requests.get(item['filePath'], allow_redirects=True)
      PATH = dir_path+'/downloads/'+item['identifier']+'/'
      if not os.path.exists(PATH):
        os.makedirs(PATH)
      open(PATH+filename, 'wb').write(r.content)

def removeAllFilesinFolder(folder):
  if os.path.exists(folder):
    for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))