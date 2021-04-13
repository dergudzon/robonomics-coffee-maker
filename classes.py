import io_funcs
import typing as tp
import ipfshttpclient
from datetime import datetime as dt
import yaml


# stores allow list values
class AllowList:
    def __init__(self, allow_list: tp.List[str], allow_list_enforced: bool = True) -> None:
        self.allow_list: tp.List[str] = allow_list
        self.allow_list_hash: str = io_funcs.allow_list_hash()
        self.allow_list_is_valid: bool = self._validate_allow_list()
        self.allow_list_enforced: bool = allow_list_enforced
        self.robonomics_allow_list_hash = io_funcs.get_robonomics_hash

    # todo
    # make a request to robonomics network in order to validate the local copy of the allow list
    def _validate_allow_list(self) -> bool:
        return self.allow_list_hash == self.robonomics_allow_list_hash

    # check, if certain ID is allowed by the policy
    def usage_allowed(self, user_id: str) -> bool:
        if not self.allow_list_enforced:
            return True
        else:
            return user_id in self.allow_list

    # todo
    # fetch allow list from ipfs
    def fetch_allow_list(self) -> None:
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

    # save a YAML session log
    def save_log(self) -> None:
        with open(f"logs/{self.session_timestamp}.yaml", "w") as log_file:
            yaml.dump(self.session_log, log_file)

    # publish the session log into ipfs
    def push_log_to_ipfs(self) -> None:
        ipfs_client = ipfshttpclient.connect()
        filename = f"logs/{self.session_timestamp}.yaml"
        res = ipfs_client.add(filename)
        self.session_log_hash = res['Hash']

    # todo
    # push hash of the session log to Robonomics network
    def push_log_hash_to_robonomics(self) -> None:
        payload = self.session_log_hash
        pass
