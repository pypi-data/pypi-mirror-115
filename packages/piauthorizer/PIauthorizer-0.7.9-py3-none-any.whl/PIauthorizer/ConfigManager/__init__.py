
import logging

from .ConfigManager import *

logging.basicConfig()
logging.Formatter("%(name)-26s - %(levelname)-8s - %(message)s")


async def override():
    return True
