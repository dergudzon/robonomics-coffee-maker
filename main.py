import rpi_funcs as rpi
import io_funcs
from classes import AllowList, CoffeeMachine
import sys
import typing as tp

# load up configuration
config: tp.Dict[str, tp.Any] = io_funcs.read_config()
if not config:
    sys.exit("Config load error")

# load up allow list
allow_list_data: tp.List[str] = io_funcs.read_allow_list()
if not allow_list_data:
    sys.exit("Allow list load error")

# initialize an instance of AllowList object
allow_list = AllowList(allow_list_data, config["use_allow_list"])

# initialize an instance of CoffeeMachine object
coffee_machine = CoffeeMachine(
    gpio_outputs=[0, 18, 0, 0, 0, 0, 0]
)

# entry point
if __name__ == "__main__":
    # start the daemon
    while True:

        # poll NFC reader until input received
        while True:
            tag_id: str = rpi.poll_nfc_reader()
            if tag_id:
                break

        # check if user is allowed to use the machine
        if not allow_list.usage_allowed(tag_id):
            print(f"UID {tag_id} is not in the allow list. Usage declined.")
            continue
        else:
            print(f"UID {tag_id} allowed. Continuing.")

        # make a coffee if usage allowed
        operation = coffee_machine.make_a_coffee()

        if operation["success"]:
            print("Operation successful.")
        else:
            print(f"Operation FAILED: {operation['message']}")
