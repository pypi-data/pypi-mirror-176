import asyncio
import logging
from logging import getLogger
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict

from AyiinXd.logger import Log


from .storage import Storage


def STORAGE(n):
    return Storage(Path("data") / n)


# Bot Logs setup:
logging.basicConfig(
    format="[%(name)s] - [%(levelname)s] - %(message)s",
    level=logging.INFO,
)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pyrogram.client").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.auth").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)

logs = getLogger(__name__)

#logs = Log(False, "ayiin.log")


CMD_HELP = {}

DEVS = [1905050903, 1965424892]


# Hosting Server

from AyiinXd.ayiin import *

HOSTED_ON = where_hosted()
