import io_funcs
import typing as tp
import ipfshttpclient
from datetime import datetime as dt
import yaml
import rpi_funcs as rpi


class AllowList:
    """stores allow list values"""

    def __init__(
        self, allow_list: tp.List[str], allow_list_enforced: bool = True
    ) -> None:
        self.allow_list: tp.List[str] = allow_list
        self.allow_list_hash: str = io_funcs.allow_list_hash()
        self.allow_list_is_valid: bool = self._validate_allow_list()
        self.allow_list_enforced: bool = allow_list_enforced
        self.robonomics_allow_list_hash = io_funcs.get_robonomics_hash

    # todo
    def _validate_allow_list(self) -> bool:
        """make a request to robonomics network in order to validate the local copy of the allow list"""

        return self.allow_list_hash == self.robonomics_allow_list_hash

    def usage_allowed(self, user_id: str) -> bool:
        """check, if certain ID is allowed to use the machine by the policy"""

        if not self.allow_list_enforced:
            return True
        else:
            return user_id in self.allow_list

    # todo
    def fetch_allow_list(self) -> None:
        """fetch allow list from ipfs"""

        ipfs_client = ipfshttpclient.connect()
        res = ipfs_client.get(self.robonomics_allow_list_hash)
        pass


class Session:
    def __init__(self, user_id: str) -> None:
        self.user_id: str = user_id
        self.session_timestamp: str = dt.now().strftime("%Y.%m.%d-%H:%M:%S")
        self.session_log: tp.Dict[str, str] = {
            "time": self.session_timestamp,
            "user_id": self.user_id,
            "status": "none"
        }
        self.session_log_hash: str = ""

    def save_log(self) -> None:
        """save a YAML session log"""

        with open(f"logs/{self.session_timestamp}.yaml", "w") as log_file:
            yaml.dump(self.session_log, log_file)

    def push_log_to_ipfs(self) -> None:
        """publish the session log into ipfs"""

        ipfs_client = ipfshttpclient.connect()
        filename = f"logs/{self.session_timestamp}.yaml"
        res = ipfs_client.add(filename)
        self.session_log_hash = res["Hash"]

    # todo
    def push_log_hash_to_robonomics(self) -> None:
        """push hash of the session log to Robonomics network"""

        payload = self.session_log_hash
        pass


class CoffeeMachine:
    """handles operating the coffee maker using RPI's GPIO"""

    def __init__(self, gpio_outputs: tp.List[int]) -> None:
        # map different control panel buttons to corresponding GPIO channels
        self.button_map: tp.Dict[str, int] = {
            "power": 0,
            "one_small_cup": 0,
            "two_small_cups": 0,
            "steam": 0,
            "rinse": 0,
            "one_big_cup": 0,
            "two_big_cups": 0
        }

        # apply provided values to their buttons
        for value in zip(gpio_outputs, self.button_map.keys()):
            if value[0]:
                self.button_map[value[1]] = value[0]

    def make_a_coffee(self) -> tp.Dict[str, tp.Any]:
        """
        pours a cup of coffee

        :returns: {"success": bool, "message": str}"""

        rpi.trigger_transistor(self.button_map["one_small_cup"])

        operation = {
            "success": True,
            "message": "operation success"
        }

        return operation
