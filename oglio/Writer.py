
from logging import Logger
from logging import getLogger

from oglio.Types import OglProject


class Writer:
    """
    A shim on top of the OGL serialization layer;  Allows me to one day replace
    the heavy-duty Python core xml minidom implementation
    Or even replace XML with JSON
    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def write(self, oglProject: OglProject, fqFileName: str):
        """

        Args:
            oglProject:     The project we have to serialize
            fqFileName:     Where to write the XML;  Should be a
        """
        pass