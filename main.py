import rpi_funcs as rpi
import io_funcs
import sys
import typing as tp
import logging

from classes import CoffeeMachine
from robonomics_daos_toolkit import acl, action_logger, substrate_connection as subcon

# set up logging
logging.basicConfig(
    level=logging.INFO,
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

# initializing all daos tools

if config["use_daos_toolkit"]:
    substrate = subcon.substrate_connection(config["daos_toolkit"]["substrate"])
    if config["daos_toolkit"]["use_acl"]:
        # initiate an instance of ACL class based on digital twin of a device
        logging.info("initiating ACL class")
        acl_obj = acl.ACL(config['daos_toolkit'], substrate)
        if not acl_obj:
            logging.critical("ACL instance error, exiting")
            sys.exit()
        else:
            logging.info("ACL initiated")
    if config["daos_toolkit"]["use_action_logger"]:
        # initiate an instance of action logger
        logging.info("initiating ActionLogger class")
        action_logger = action_logger.ActionLogger(config['daos_toolkit'], substrate)
        if not action_logger:
            logging.critical("ActionLogger instance error, exiting")
            sys.exit()
        else:
            logging.info("ActionLogger initiated")

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

        if config["daos_toolkit"]["use_acl"]:
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
            if config["daos_toolkit"]["use_action_logger"]:
                action_logger.log_action(f"Making coffee for {tag_id}", "success")
        else:
            logging.error(f"Operation FAILED: {operation['message']}")
            if config["daos_toolkit"]["use_action_logger"]:
                action_logger.log_action(f"Making coffee for {tag_id}", "failure")

        logging.info("Session over")
