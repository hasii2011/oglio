
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from dataclasses import field

from ogl.OglClass import OglClass
from ogl.OglObject import OglObject
from ogl.OglLink import OglLink
from ogl.OglInterface2 import OglInterface2

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import Documents
from untanglepyut.UnTangler import UnTangler
from untanglepyut.UnTangler import ProjectInformation


OglClasses = NewType('OglClasses', List[OglClass])
OglLinks   = NewType('OglLinks',   List[OglLink])

OglObjects = Union[List[OglObject], OglClasses, OglLinks, List[OglInterface2]]


def createOglClassesFactory() -> OglClasses:
    """
    Factory method to create  the OglClasses data structure;

    Returns:  A new data structure
    """
    return OglClasses([])


def createOglLinksFactory() -> OglLinks:
    """
    Factory method to create  the OglLinks data structure;

    Returns:  A new data structure
    """
    return OglLinks([])


OglDocumentTitle = NewType('OglDocumentTitle', str)


@dataclass
class OglDocument:
    documentType:    str = ''
    documentTitle:   OglDocumentTitle = OglDocumentTitle('')
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses:       OglClasses = field(default_factory=createOglClassesFactory)
    oglLinks:         OglLinks   = field(default_factory=createOglLinksFactory)

    def toOglDocument(self, document: Document):
        self.documentType    = document.documentType
        self.documentTitle   = OglDocumentTitle(document.documentTitle)
        self.scrollPositionX = document.scrollPositionX
        self.scrollPositionY = document.scrollPositionY
        self.pixelsPerUnitX  = document.pixelsPerUnitX
        self.pixelsPerUnitY  = document.pixelsPerUnitY


OglDocuments     = NewType('OglDocuments', dict[OglDocumentTitle, OglDocument])


def createOglDocumentsFactory() -> OglDocuments:
    return OglDocuments({})


@dataclass
class OglProject:
    version:  str = cast(str, None)
    codePath: str = cast(str, None)
    oglDocuments: OglDocuments = field(default_factory=createOglDocumentsFactory)

    def toOglProject(self, project: ProjectInformation):
        self.version  = project.version
        self.codePath = project.codePath


class Reader:
    """
    This is a simple translation layer on top of the PyutUntangler library.  This
    layer simply hides that implementation detail and provides a more usable
    interface to Pyut.  Additionally, it serve as a common piece of code
    that allows and IOPlugin implementation
    See https://github.com/hasii2011/pyutplugincore
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)
        self.logger: Logger = getLogger(__name__)

    def read(self, fqFileName: str) -> OglProject:

        """
        Parse the input XML file

        Args:
            fqFileName: Fully qualified file name
        """
        untangler: UnTangler = UnTangler(fqFileName=fqFileName)

        untangler.untangle()

        oglProject: OglProject = OglProject()

        oglProject.toOglProject(untangler.projectInformation)

        documents: Documents = untangler.documents
        for document in documents.values():
            self.logger.info(f'Untangled - {document.documentTitle}')
            oglDocument: OglDocument = OglDocument()
            oglDocument.toOglDocument(document)
            #
            # Cheat by just type casting
            #
            oglDocument.oglClasses = cast(OglClasses, document.oglClasses)
            oglDocument.oglLinks   = cast(OglLinks, document.oglLinks)

            self.logger.info(f'OglDocument - {oglDocument}')
            oglProject.oglDocuments[oglDocument.documentTitle] = oglDocument

        return oglProject
