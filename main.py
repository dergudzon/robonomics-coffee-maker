import rpi_funcs as rpi
import io_funcs
from classes import AllowList, CoffeeMachine
import sys
import typing as tp
import logging

# set up logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="daemon.log",
    format="%(asctime)s %(levelname)s: %(message)s"
)

# load up configuration
config: tp.Dict[str, tp.Any] = io_funcs.read_config()
if not config:
    logging.critical("Config load error, exiting")
    sys.exit()
else:
    logging.info("Config load successful")

# load up allow list
if config["use_allow_list"]:
    allow_list_data: tp.List[str] = io_funcs.read_allow_list()
    if not allow_list_data:
        logging.critical("Allow list load error, exiting")
        sys.exit()
    else:
        # initialize an instance of AllowList object
        allow_list = AllowList(allow_list_data, config["use_allow_list"])
        logging.info("Allow list load successful")


# initialize an instance of CoffeeMachine object
coffee_machine = CoffeeMachine(
    gpio_outputs=[0, 21, 0, 0, 0, 0, 0]
)

# entry point
if __name__ == "__main__":
    logging.info("Daemon started")

    # start the daemon
    while True:

        # poll NFC reader until input received
        logging.info("Start polling NFC reader")
        while True:
            tag_id: str = rpi.poll_nfc_reader()
            if tag_id:
                logging.info(f"Found NFC tag with UID {tag_id}. Stopped polling")
                break

        if config["use_allow_list"]:
            # check if user is allowed to use the machine
            if not allow_list.usage_allowed(tag_id):
                logging.warning(f"UID {tag_id} is not in the allow list. Usage declined.")
                continue
            else:
                logging.info(f"UID {tag_id} allowed. Continuing.")

        # make a coffee if usage allowed
        operation = coffee_machine.make_a_coffee()

        if operation["success"]:
            logging.info("Operation successful.")
        else:
            logging.error(f"Operation FAILED: {operation['message']}")

        logging.info("Session over")
