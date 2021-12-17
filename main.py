import sys
import logging
import configparser

from classes import SaecoCoffeeMachine
from robonomicsinterface import RobonomicsInterface as RI
from statemine_monitor import ACTIncomeTracker
from substrateinterface import Keypair


def read_config(path: str) -> Keypair:
    config = configparser.ConfigParser()
    config.read(path)
    mnemonic = config.get('secrets', 'MNEMONIC_SEED')
    keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=32)
    return keypair


def main(config, coffee_name):
    # set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    # initialize an instance of CoffeeMachine object
    coffee_machine = SaecoCoffeeMachine()

    # Start income tracker
    # income_tracker = ACTIncomeTracker(keypair.ss58_address)

    # Start coffee machine daemon
    logging.info("Started main coffee machine daemon")
    # while True:
        # wait for money income event
        # income_tracker.act_income_event.wait()
        # income_tracker.act_income_event.clear()
    operation = coffee_machine.make_a_coffee(coffee_name)

    if operation["success"]:
        logging.info("Operation Successful.")
        try:
            # Initiate RobonomicsInterface instance
            ri_interface = RI(seed=config['mnemonic'])
            ri_interface.record_datalog(f"Successfully made some coffee!")
        except Exception as e:
            logging.error(f"Failed to record Datalog: {e}")
    else:
        logging.error(f"Operation Failed.")
        try:
            # Initiate RobonomicsInterface instance
            ri_interface = RI(seed=config['mnemonic'])
            ri_interface.record_datalog(f"Failed to make coffee: {operation['message']}")
        except Exception as e:
            logging.error(f"Failed to record Datalog: {e}")
    logging.info("Session over")


if __name__:
    config = read_config('config.config')
    coffee_name: str = sys.argv[1]
    main(config, coffee_name)