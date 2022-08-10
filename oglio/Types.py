
from dataclasses import dataclass
from dataclasses import field

from typing import List
from typing import NewType
from typing import Union
from typing import cast

from ogl.OglObject import OglObject
from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink

from untanglepyut.UnTangler import Document
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
