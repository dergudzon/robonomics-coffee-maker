# functions which refer to hardware operation of a host machine (Raspberry Pi)
import subprocess
from gpiozero import LED
from time import sleep
import logging

# set up logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="daemon.log",
    format="%(asctime)s %(levelname)s: %(message)s"
)


def poll_nfc_reader() -> str:
    """
    polls nfc reader using libnfc cli interface.
    polling has to be reinitialized every 36 seconds.

    :return: UID of an NFC tag if found one
    """

    command = "sudo nfc-poll | grep UID | cut -d : -f 2"
    output = subprocess.getoutput(command)
    if output:
        tag_id = output.split("\n")[1].strip()
        return tag_id
    else:
        return ""


def trigger_transistor(channel: int = 18) -> None:
    """trigger a transistor on a specified GPIO channel"""

    logging.info(f"Triggering GPIO{channel} for 0.3s")
    transistor = LED(channel)

    transistor.on()
    sleep(0.3)
    transistor.off()

    return None
