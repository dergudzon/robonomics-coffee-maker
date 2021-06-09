import yaml
import typing as tp
from os import path
import logging

# set up logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="daemon.log",
    format="%(asctime)s %(levelname)s: %(message)s"
)


def read_config() -> tp.Dict[str, tp.Any]:
    """load up the configuration file"""

    if not path.exists("config.yaml"):
        logging.error("config.yaml not found")
        return {}

    with open("config.yaml", "r") as file:
        try:
            return yaml.safe_load(file)
        except Exception as E:
            logging.error(f"Error loading config.yaml: {E}")
            return {}
