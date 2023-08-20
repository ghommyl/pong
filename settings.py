import json
import logging

filename = "settings.json"
file = open(filename)
settings = json.load(file)
file.close()

logging.info("settings.json loaded")
for key, value in settings.items():
    logging.debug(f"{key}: {value}")
