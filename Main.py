from PermData import PermStorage
from Logger import Logger

permDict = PermStorage().get_dictionary()  # permanent storage set up
logger = Logger(permDict)

logger.add_log("some text", "main", "no account")