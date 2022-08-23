
from typing import Tuple
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from pyutmodel.PyutActor import PyutActor

from pyutmodel.PyutClassCommon import PyutClassCommon
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage
from pyutmodel.PyutText import PyutText
from pyutmodel.PyutUseCase import PyutUseCase

from ogl.OglActor import OglActor
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase
from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglTexts
from oglio.Types import OglUseCases
from oglio.toXmlV10.BaseOglToMiniDom import BaseOglToMiniDom
from oglio.toXmlV10.OglClassesToMiniDom import OglClassesToMiniDom
from oglio.toXmlV10.OglLinksToMiniDom import OglLinksToMiniDom
from oglio.toXmlV10.OglUseCasesToMiniDom import OglUseCasesToMiniDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglToMiniDom(BaseOglToMiniDom):
    """
    The refactored version of the original methods that were part of the monolithic
     PyutXml`xxx` classes.

     This version is
        * renamed for clarity
        * uses typing for developer clarity
        * removes 'magic' strings shared between it and the ToOgl/ToPyutXml classes
        * Updated using google docstrings

    """
    ORIGINAL_XML_PROLOG: str = '<?xml version="1.0" ?>'
    FIXED_XML_PROLOG:    str = '<?xml version="1.0" encoding="iso-8859-1"?>'

    def __init__(self, projectVersion: str, projectCodePath: str):
        """

        Args:
            projectVersion:
            projectCodePath:
        """

        self.logger:     Logger    = getLogger(__name__)

        xmlDocument, topElement = self._createStarterXmlDocument(projectVersion=projectVersion, projectCodePath=projectCodePath)

        super().__init__(xmlDocument=xmlDocument)

        self._topElement:  Element  = topElement

        self._oglClassesToMiniDom:  OglClassesToMiniDom  = OglClassesToMiniDom(xmlDocument=self._xmlDocument)
        self._oglLinksToMiniDom:    OglLinksToMiniDom    = OglLinksToMiniDom(xmlDocument=self._xmlDocument)
        self._oglUseCasesToMiniDom: OglUseCasesToMiniDom = OglUseCasesToMiniDom(xmlDocument=self._xmlDocument)

    @property
    def xmlDocument(self) -> Document:
        """
        Presumably used to persist the document

        Returns:  The serialized Document
        """
        return self._xmlDocument

    def serialize(self, oglDocument: OglDocument):

        documentNode: Element = self._oglDocumentToXml(oglDocument=oglDocument)

        self._topElement.appendChild(documentNode)

        oglClasses:  OglClasses  = cast(OglClasses, oglDocument.oglClasses)
        oglLinks:    OglLinks    = cast(OglLinks, oglDocument.oglLinks)
        oglUseCases: OglUseCases = cast(OglUseCases, oglDocument.oglUseCases)
        oglActors:   OglActors   = cast(OglActors, oglDocument.oglActors)

        documentNode = self._oglClassesToMiniDom.serialize(documentNode=documentNode, oglClasses=oglClasses)
        documentNode = self._oglUseCasesToMiniDom.serialize(documentNode=documentNode, oglUseCases=oglUseCases, oglActors=oglActors)
        documentNode = self._oglLinksToMiniDom.serialize(documentNode=documentNode, oglLinks=oglLinks)

        oglTexts: OglTexts = cast(OglTexts, oglDocument.oglTexts)
        for oglText in oglTexts:
            textElement: Element = self._oglTextToXml(oglText, xmlDoc=self._xmlDocument)
            documentNode.appendChild(textElement)

    def writeXml(self, fqFileName):
        """
        Persist the XML

        Args:
            fqFileName:  The fully qualified file name
        """

        xmlText: str = self._xmlDocument.toprettyxml()
        updatedXml: str = OglToMiniDom.setAsISOLatin(xmlText)

        with open(fqFileName, 'w') as fd:
            fd.write(updatedXml)

    @classmethod
    def setAsISOLatin(cls, xmlTextToUpdate: str) -> str:
        """
        Add attribute encoding = "iso-8859-1" this is not possible with minidom, so we use pattern matching

        Args:
            xmlTextToUpdate:  Old XML

        Returns:  Updated XML
        """
        retText: str = xmlTextToUpdate.replace(OglToMiniDom.ORIGINAL_XML_PROLOG, OglToMiniDom.FIXED_XML_PROLOG)
        return retText

    def oglNoteToXml(self, oglNote: OglNote, xmlDoc: Document) -> Element:
        """
        Export an OglNote to a minidom Element.

        Args:
            oglNote:    Note to convert
            xmlDoc:     xml document

        Returns:
            New minidom element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_NOTE)

        self._appendOglBase(oglNote, root)

        root.appendChild(self._pyutNoteToXml(cast(PyutNote, oglNote.pyutObject), xmlDoc))

        return root

    def _oglTextToXml(self, oglText: OglText, xmlDoc: Document) -> Element:

        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_TEXT)

        self._appendOglBase(oglText, root)

        root.setAttribute(XmlConstants.ATTR_TEXT_SIZE, str(oglText.textSize))
        root.setAttribute(XmlConstants.ATTR_IS_BOLD, str(oglText.isBold))
        root.setAttribute(XmlConstants.ATTR_IS_ITALICIZED, str(oglText.isItalicized))
        root.setAttribute(XmlConstants.ATTR_FONT_FAMILY, oglText.textFontFamily.value)

        root.appendChild(self._pyutTextToXml(oglText.pyutText, xmlDoc))

        return root

    def oglSDInstanceToXml(self, oglSDInstance: OglSDInstance, xmlDoc: Document) -> Element:
        """
        Export an OglSDInstance to a minidom Element

        Args:
            oglSDInstance:  Instance to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_SD_INSTANCE)

        self._appendOglBase(oglSDInstance, root)

        root.appendChild(self._pyutSDInstanceToXml(cast(PyutSDInstance, oglSDInstance.pyutObject), xmlDoc))

        return root

    def oglSDMessageToXml(self, oglSDMessage: OglSDMessage, xmlDoc: Document) -> Element:
        """
        Export an OglSDMessage to a minidom Element.

        Args:
            oglSDMessage:   Message to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_SD_MESSAGE)

        # adding the data layer object
        root.appendChild(self._pyutSDMessageToXml(oglSDMessage.getPyutObject(), xmlDoc))

        return root

    def _pyutClassCommonToXml(self, classCommon: PyutClassCommon, root: Element) -> Element:

        root.setAttribute(XmlConstants.ATTR_DESCRIPTION, classCommon.description)
        # root.setAttribute(PyutXmlConstants.ATTR_FILENAME,    pyutInterface.getFilename())

        return root

    def _pyutMethodToXml(self, pyutMethod, xmlDoc) -> Element:
        """
        Exporting a PyutMethod to a miniDom Element

        Args:
            pyutMethod: Method to save
            xmlDoc:     xml document

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_METHOD)

        root.setAttribute(XmlConstants.ATTR_NAME, pyutMethod.name)

        visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
        visName:    str                = self.__safeVisibilityToName(visibility)

        if visibility is not None:
            root.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)

        for modifier in pyutMethod.modifiers:
            xmlModifier: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_MODIFIER)
            xmlModifier.setAttribute(XmlConstants.ATTR_NAME, modifier.name)
            root.appendChild(xmlModifier)

        if pyutMethod.returnType is not None:
            xmlReturnType: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_RETURN)
            xmlReturnType.setAttribute(XmlConstants.ATTR_TYPE, str(pyutMethod.returnType))
            root.appendChild(xmlReturnType)

        for param in pyutMethod.parameters:
            root.appendChild(self._pyutParamToXml(param, xmlDoc))

        codeRoot: Element = self._pyutSourceCodeToXml(pyutMethod.sourceCode, xmlDoc)
        root.appendChild(codeRoot)
        return root

    def _pyutSourceCodeToXml(self, sourceCode: SourceCode, xmlDoc: Document) -> Element:

        codeRoot: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_SOURCE_CODE)
        for code in sourceCode:
            codeElement:  Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_CODE)
            textCodeNode: Element = xmlDoc.createTextNode(code)
            codeElement.appendChild(textCodeNode)
            codeRoot.appendChild(codeElement)

        return codeRoot

    def _pyutParamToXml(self, pyutParam: PyutParameter, xmlDoc: Document) -> Element:
        """
        Export a PyutParam to a miniDom Element

        Args:
            pyutParam:  Parameter to save
            xmlDoc:     XML Node

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_PARAM)

        root.setAttribute(XmlConstants.ATTR_NAME, pyutParam.name)
        root.setAttribute(XmlConstants.ATTR_TYPE, str(pyutParam.type))

        defaultValue = pyutParam.defaultValue
        if defaultValue is not None:
            root.setAttribute(XmlConstants.ATTR_DEFAULT_VALUE, defaultValue)

        return root

    def _pyutNoteToXml(self, pyutNote: PyutNote, xmlDoc: Document) -> Element:
        """
        Export a PyutNote to a miniDom Element.

        Args:
            pyutNote:   Note to convert
            xmlDoc:     xml document

        Returns:
            New miniDom element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_NOTE)

        noteId: int = self._idFactory.getID(pyutNote)
        root.setAttribute(XmlConstants.ATTR_ID, str(noteId))

        content: str = pyutNote.content
        content = content.replace('\n', "\\\\\\\\")
        root.setAttribute(XmlConstants.ATTR_CONTENT, content)

        root.setAttribute(XmlConstants.ATTR_FILENAME, pyutNote.fileName)

        return root

    def _pyutTextToXml(self, pyutText: PyutText, xmlDoc: Document) -> Element:

        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_TEXT)
        textId: int = self._idFactory.getID(pyutText)

        root.setAttribute(XmlConstants.ATTR_ID, str(textId))
        content: str = pyutText.content
        content = content.replace('\n', "\\\\\\\\")

        root.setAttribute(XmlConstants.ATTR_CONTENT, content)

        return root

    def _pyutSDInstanceToXml(self, pyutSDInstance: PyutSDInstance, xmlDoc: Document) -> Element:
        """
        Exporting a PyutSDInstance to an minidom Element.

        Args:
            pyutSDInstance:     Class to convert
            xmlDoc:             xml document

        Returns:
            A new minidom element
        """
        root:  Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_SD_INSTANCE)
        eltId: int     = self._idFactory.getID(pyutSDInstance)

        root.setAttribute(XmlConstants.ATTR_ID, str(eltId))
        root.setAttribute(XmlConstants.ATTR_INSTANCE_NAME, pyutSDInstance.instanceName)
        root.setAttribute(XmlConstants.ATTR_LIFE_LINE_LENGTH, str(pyutSDInstance.instanceLifeLineLength))

        return root

    def _pyutSDMessageToXml(self, pyutSDMessage: PyutSDMessage, xmlDoc: Document) -> Element:
        """
        Exporting a PyutSDMessage to an minidom Element.
        Args:
            pyutSDMessage:  SDMessage to export
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_SD_MESSAGE)

        eltId = self._idFactory.getID(pyutSDMessage)
        root.setAttribute(XmlConstants.ATTR_ID, str(eltId))

        # message
        root.setAttribute(XmlConstants.ATTR_MESSAGE, pyutSDMessage.getMessage())

        # time
        idSrc = self._idFactory.getID(pyutSDMessage.getSource())
        idDst = self._idFactory.getID(pyutSDMessage.getDest())
        root.setAttribute(XmlConstants.ATTR_SOURCE_TIME_LINE, str(pyutSDMessage.getSrcTime()))
        root.setAttribute(XmlConstants.ATTR_DESTINATION_TIME_LINE, str(pyutSDMessage.getDstTime()))
        root.setAttribute(XmlConstants.ATTR_SD_MESSAGE_SOURCE_ID, str(idSrc))
        root.setAttribute(XmlConstants.ATTR_SD_MESSAGE_DESTINATION_ID, str(idDst))

        return root

    def __safeVisibilityToName(self, visibility: Union[str, PyutVisibilityEnum]) -> str:
        """
        Account for old pre V10 code
        Args:
            visibility:

        Returns:
            The visibility name
        """

        if isinstance(visibility, str):
            visStr: str = PyutVisibilityEnum.toEnum(visibility).name
        else:
            visStr = visibility.name

        return visStr

    def _createStarterXmlDocument(self, projectVersion: str, projectCodePath: str) -> Tuple[Document, Element]:

        xmlDocument: Document = Document()

        topElement: Element = xmlDocument.createElement(XmlConstants.TOP_LEVEL_ELEMENT)

        topElement.setAttribute(XmlConstants.ATTR_VERSION, projectVersion)
        topElement.setAttribute(XmlConstants.ATTR_CODE_PATH, projectCodePath)

        xmlDocument.appendChild(topElement)

        return xmlDocument, topElement

    def _oglDocumentToXml(self, oglDocument: OglDocument) -> Element:

        documentNode = self._xmlDocument.createElement(XmlConstants.ELEMENT_DOCUMENT)

        documentNode.setAttribute(XmlConstants.ATTR_TYPE, oglDocument.documentType)
        documentNode.setAttribute(XmlConstants.ATTR_TITLE, oglDocument.documentTitle)

        documentNode.setAttribute(XmlConstants.ATTR_SCROLL_POSITION_X, str(oglDocument.scrollPositionX))
        documentNode.setAttribute(XmlConstants.ATTR_SCROLL_POSITION_Y, str(oglDocument.scrollPositionY))

        documentNode.setAttribute(XmlConstants.ATTR_PIXELS_PER_UNIT_X, str(oglDocument.pixelsPerUnitX))
        documentNode.setAttribute(XmlConstants.ATTR_PIXELS_PER_UNIT_Y, str(oglDocument.pixelsPerUnitY))

        return documentNode
