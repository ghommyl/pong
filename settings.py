import json
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)-7s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

filename = "settings.json"
file = open(filename)
settings = json.load(file)
file.close()

logging.info("settings.json loaded")
for key, value in settings.items():
    logging.debug(f"{key}: {value}")
