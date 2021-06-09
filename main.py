import rpi_funcs as rpi
import io_funcs
from robonomics_daos_toolkit.acl import ACL
from classes import CoffeeMachine
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
    logging.info(f"Config load successful\n{config}")

# initialize an instance of CoffeeMachine object
coffee_machine = CoffeeMachine(
    gpio_outputs=[0, 21, 0, 0, 0, 0, 0]
)

if config["use_acl"]:
    # initiate an instance of ACL class based on digital twin of a device
    logging.info("initiating ACL class")
    acl_obj = ACL(config['robonomics'])
    if not acl_obj:
        logging.critical("ACL instance error, exiting")
        sys.exit()
    else:
        logging.info("ACL initiated")

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

        if config["use_acl"]:
            # check if user is allowed to use the machine
            if not acl_obj.usage_allowed(tag_id):
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
