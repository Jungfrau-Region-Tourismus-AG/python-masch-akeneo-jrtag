# Update to MASCH all 5 minutes

import sys
sys.path.append("..")

import service.masch as masch
import service.contentdesk as contentdesk
    
def __main__():
    print("STARTING - WORKER")
    masch.maschFlow()
    contentdesk.contentdeskFlow()
    print("END - WORKER")
    
if __name__== "__main__":
    __main__()