import logging


from src.config.settings import LOG_LEVEL
 

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger("AI-Document-Chat")