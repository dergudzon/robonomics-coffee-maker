import ipfshttpclient
from hashlib import sha256
import yaml
import typing as tp
from os import path


def read_config() -> tp.Dict[str, tp.Any]:
    """load up the configuration file"""

    if not path.exists("config.yaml"):
        print("config.yaml not found")
        return {}

    with open("config.yaml", "r") as file:
        try:
            return yaml.safe_load(file)["config"]
        except Exception as E:
            print(f"Error loading config.yaml: {E}")
            return {}


def read_allow_list() -> tp.List[str]:
    """load up the allow list"""

    if not path.exists("allow_list.yaml"):
        print("allow_list.yaml not found")
        return []

    with open("allow_list.yaml", "r") as file:
        try:
            return yaml.safe_load(file)["allowed_ids"]
        except Exception as E:
            print(f"Error loading allow_list.yaml: {E}")
            return []


def allow_list_hash() -> str:
    """get an sha256 checksum of the allow_list.yaml file"""

    with open("allow_list.yaml", "rb") as file:
        allow_list_bytes = file.read()
        check_sum = sha256(allow_list_bytes).hexdigest()
        return check_sum


# todo
def get_robonomics_hash() -> str:
    """gets the latest hash for an allow list from robonomics network"""

    pass
