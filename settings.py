import json
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)-10s- %(message)s")

filename = "settings.json"
file = open(filename)
settings = json.load(file)
file.close()

logging.info("settings.json loaded")
logging.debug(f"settings.json: {settings}")
