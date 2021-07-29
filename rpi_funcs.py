# functions which refer to hardware operation of a host machine (Raspberry Pi)
from gpiozero import LED
from time import sleep
import logging

# set up logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="daemon.log",
    format="%(asctime)s %(levelname)s: %(message)s"
)


def trigger_transistor(channel: int = 18) -> None:
    """trigger a transistor on a specified GPIO channel"""

    logging.info(f"Triggering GPIO{channel} for 0.3s")
    transistor = LED(channel)

    transistor.on()
    sleep(0.3)
    transistor.off()

    return None
