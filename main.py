import rpi_funcs
import io_funcs
from classes import AllowList
import sys
import typing as tp

# load up configuration
config: tp.Dict[str, str] = io_funcs.read_config()
if not config:
    sys.exit("Config load error")

# load up allow list
allow_list_data: tp.List[str] = io_funcs.read_allow_list()
if not allow_list_data:
    sys.exit("Allow list load error")

# initialize an instance of AllowList object
allow_list = AllowList(allow_list_data, config["use_allow_list"])

# entry point
if __name__ == "__main__":
    while True:
        pass
