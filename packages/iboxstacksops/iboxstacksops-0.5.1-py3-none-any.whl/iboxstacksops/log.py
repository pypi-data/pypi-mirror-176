import logging


logging.basicConfig()
logging.getLogger("botocore").setLevel("CRITICAL")
logger = logging.getLogger("stacksops")
logger.setLevel(logging.INFO)
