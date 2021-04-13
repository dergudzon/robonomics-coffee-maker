import io_funcs
import typing as tp


# stores allow list values
class AllowList:
    def __init__(self, allow_list: tp.List[str], allow_list_enforced: bool = True) -> None:
        self.allow_list: tp.List[str] = allow_list
        self.allow_list_hash: str = io_funcs.allow_list_hash()
        self.allow_list_is_valid: bool = self._validate_allow_list()
        self.allow_list_enforced: bool = allow_list_enforced

    # todo
    # make a request to robonomics network in order to validate the local copy of the allow list
    def _validate_allow_list(self) -> bool:
        # robonomics_allow_list_hash = io_funcs.get_robonomics_hash
        # return self.allow_list_hash == robonomics_allow_list_hash
        return True

    def usage_allowed(self, user_id: str) -> bool:
        if not self.allow_list_enforced:
            return True
        else:
            return user_id in self.allow_list
