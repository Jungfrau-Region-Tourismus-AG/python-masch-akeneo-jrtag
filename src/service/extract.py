from os import getenv
from dotenv import find_dotenv, load_dotenv
from akeneo.akeneo import Akeneo
import requests
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


def getMaschPull():
  url = MASCH_URL + MASCH_PULL_URL
  body = {
      "user_login": MASCH_USER,
      "user_password": MASCH_PASSWORD
  }
  r = requests.get(url, json=body)
  print(r.status_code)
  return r.json()

def getAkeneoProducts():
  akeneo = Akeneo(
    AKENEO_HOST,
    AKENEO_CLIENT_ID,
    AKENEO_CLIENT_SECRET,
    AKENEO_USERNAME,
    AKENEO_PASSWORD
  )
  searchQuery = '{"maschId":[{"operator":"NOT EMPTY","value":""}]}'
  return akeneo.getProducts(limit=100, search=searchQuery )

def extract():
  data = getMaschPull()
  return data