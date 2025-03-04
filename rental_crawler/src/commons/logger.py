from logging import getLogger, Formatter, StreamHandler

from config import LOG_LEVEL


formatter = Formatter("%(asctime)s - %(name)s - [%(levelname)s] -> %(message)s")

ch = StreamHandler()
ch.setLevel(LOG_LEVEL)
ch.setFormatter(formatter)

logger = getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(ch)
