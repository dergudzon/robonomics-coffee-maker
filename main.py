import sys
import typing as tp
import logging

from classes import CoffeeMachine
from robonomics_daos_toolkit import acl, action_logger, obtain_incomes, common_utils as cu

# set up logging
logging.basicConfig(
    level=logging.INFO,
    filename="daemon.log",
    format="%(asctime)s %(levelname)s: %(message)s"
)

# load up configuration
config: tp.Dict[str, tp.Any] = cu.read_yaml_file("config.yaml")

# connect to substrate
substrate = cu.substrate_connection(config["daos_toolkit"]["substrate"])

# initialize an instance of CoffeeMachine object
coffee_machine = CoffeeMachine(
    gpio_outputs=[0, 21, 0, 0, 0, 0, 0]
)


# initializing all daos tools
if config["use_daos_toolkit"]:

    if config["daos_toolkit"]["use_acl"]:
        # initiate an instance of ACL class based on digital twin of a device
        acl_obj = acl.ACL(config["daos_toolkit"], cu.substrate_connection(config["daos_toolkit"]["substrate"]))
        if not acl_obj:
            sys.exit()

    if config["daos_toolkit"]["use_action_logger"]:
        # initiate an instance of action logger
        action_logger = action_logger.ActionLogger(config["daos_toolkit"],
                                                   cu.substrate_connection(config["daos_toolkit"]["substrate"]))
        if not action_logger:
            sys.exit()

logging.info("Coffee machine daemon started")

# start the daemon
income_tracker = obtain_incomes.IncomeTracker(config["daos_toolkit"], substrate)

while True:
    # wait for money income event
    income_tracker.money_income_event.wait()
    income_tracker.money_income_event.clear()

    if config["daos_toolkit"]["use_acl"]:
        # check if user is allowed to use the machine
        if not acl_obj.usage_allowed(income_tracker.money_income_event.source_address):
            logging.warning(f"Account {income_tracker.money_income_event.source_address} is not in the allow list. "
                            f"Usage declined. Thanks for the money")
            continue
        else:
            logging.info(f"Account {income_tracker.money_income_event.source_address} allowed. Continuing.")

    # Coffee making part
    operation = coffee_machine.make_a_coffee()

    if operation["success"]:

        logging.info("Operation successful.")
        if config["daos_toolkit"]["use_action_logger"]:
            action_logger.log_action(f"Making coffee for {income_tracker.money_income_event.source_address}.",
                                     "success")
    else:

        logging.error(f"Operation FAILED.")
        if config["daos_toolkit"]["use_action_logger"]:
            action_logger.log_action(f"Making coffee for {income_tracker.money_income_event.source_address}.",
                                     "FAILURE: " + operation["message"])

    logging.info("Session over")
