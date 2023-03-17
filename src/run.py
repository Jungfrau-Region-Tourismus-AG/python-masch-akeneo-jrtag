import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

def __main__():
  print("Hello Word i run from run.py!")
  print(os.environ['SECRET_TEST'])

if __name__== "__main__":
    __main__()