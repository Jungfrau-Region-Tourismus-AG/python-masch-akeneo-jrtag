# Update to MASCH all 5 minutes

import sys
sys.path.append("..")

import service.masch as masch
import service.contentdeskFlow as contentdeskFlow
    
def __main__():
    print("STARTING - WORKER")
    masch.maschFlow()
    contentdeskFlow.contentdeskFlow()
    print("END - WORKER")
    
if __name__== "__main__":
    __main__()