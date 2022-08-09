
from logging import Logger
from logging import getLogger


class Writer:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)