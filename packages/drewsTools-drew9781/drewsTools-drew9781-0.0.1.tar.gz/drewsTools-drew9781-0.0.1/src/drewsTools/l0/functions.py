import json
import yaml
import logging
logger = logging.getLogger(__name__)

def readFile(**kwargs):
    filename = kwargs.get("filename")
    filetype = kwargs.get("filetype")

    if (filetype == "json"):
        try:
            with open(filename) as f:
                logger.debug("read json file: "+ filename)
                data = json.load(f)
                return (data)
        except:
            #didnt find file
            raise Exception("failed to read file "+filename)
    elif (filetype == "yaml"):
        try:
            with open(filename) as f:
                logger.debug("read yaml file: "+ filename)
                data = yaml.safe_load(f)
                return (data)
        except:
            #didnt find file
            raise Exception("failed to read file "+filename)

def getCreds(**kwargs):
    filename = kwargs.get("filename")
    return readFile(filename=filename, filetype="json")