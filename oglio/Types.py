
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from dataclasses import dataclass
from dataclasses import field

from ogl.OglActor import OglActor
from ogl.OglNote import OglNote
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import ProjectInformation

OglClasses  = NewType('OglClasses',  List[OglClass])
OglLinks    = NewType('OglLinks',    List[OglLink])
OglNotes    = NewType('OglNotes',    List[OglNote])
OglTexts    = NewType('OglTexts',    List[OglText])
OglActors   = NewType('OglActors',   List[OglActor])
OglUseCases = NewType('OglUseCases', List[OglUseCase])

OglObjects = Union[OglClasses, OglLinks, OglNotes, OglTexts, OglActors, OglUseCases]


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


def createOglNotesFactory() -> OglNotes:
    return OglNotes([])


def createOglTextsFactory() -> OglTexts:
    return OglTexts([])


def createOglActorsFactory() -> OglActors:
    return OglActors([])


def createOglUseCasesFactory() -> OglUseCases:
    return OglUseCases([])


OglDocumentTitle = NewType('OglDocumentTitle', str)


@dataclass
class OglDocument:
    documentType:    str = ''
    documentTitle:   OglDocumentTitle = OglDocumentTitle('')
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses:      OglClasses  = field(default_factory=createOglClassesFactory)
    oglLinks:        OglLinks    = field(default_factory=createOglLinksFactory)
    oglNotes:        OglNotes    = field(default_factory=createOglNotesFactory)
    oglTexts:        OglTexts    = field(default_factory=createOglTextsFactory)
    oglActors:       OglActors   = field(default_factory=createOglActorsFactory)
    oglUseCases:     OglUseCases = field(default_factory=createOglUseCasesFactory)

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