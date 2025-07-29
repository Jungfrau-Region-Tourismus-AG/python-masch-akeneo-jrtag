# Full Update to MASCH

import sys
sys.path.append("..")

import service.maschFlow as maschFlow
import service.contentdeskFlow as contentdeskFlow
    
def __main__():
    print("STARTING - WORKER")
    maschFlow.maschFlow()
    contentdeskFlow.contentdeskFullFlow()
    print("END - WORKER")
    
if __name__== "__main__":
    __main__()