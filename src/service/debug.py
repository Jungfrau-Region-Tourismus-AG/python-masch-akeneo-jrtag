import json
from datetime import datetime
import logging
import os

# DEBUG - Full
def addToFileFull(mainpath, environment, folder, attribute, name, data):
    # get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    #print("Current date & time : ", current_datetime)
    
    # convert datetime obj to string
    str_current_datetime = str(current_datetime)
    
    if attribute != "":
        # Check if folder exists
        if not os.path.exists("../../output/"+mainpath+"/"+environment+"/"+folder+"/"+attribute+"/"+str_current_datetime+"/"):
            os.makedirs("../../output/"+mainpath+"/"+environment+"/"+folder+"/"+attribute+"/"+str_current_datetime+"/")
        
        with open("../../output/"+mainpath+"/"+environment+"/"+folder+"/"+attribute+"/"+str_current_datetime+"/"+name+".json", "w") as file:
            file.write(json.dumps(data))
    else:
        # Check if folder exists
        if not os.path.exists("../../output/"+mainpath+"/"+environment+"/"+str_current_datetime+"/"):
            os.makedirs("../../output/"+mainpath+"/"+environment+"/"+str_current_datetime+"/")
        
        with open("../../output/"+mainpath+"/"+environment+"/"+str_current_datetime+"/"+name+".json", "w") as file:
            file.write(json.dumps(data))