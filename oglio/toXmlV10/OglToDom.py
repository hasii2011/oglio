
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage
from pyutmodel.PyutText import PyutText

from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages
from oglio.Types import OglTexts
from oglio.Types import OglUseCases
from oglio.toXmlV10.BaseOglToDom import BaseOglToDom
from oglio.toXmlV10.OglClassesToDom import OglClassesToDom
from oglio.toXmlV10.OglLinksToDom import OglLinksToDom
from oglio.toXmlV10.OglUseCasesToDom import OglUseCasesToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglToDom(BaseOglToDom):
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

        self._oglClassesToMiniDom:  OglClassesToDom  = OglClassesToDom(xmlDocument=self._xmlDocument)
        self._oglLinksToMiniDom:    OglLinksToDom    = OglLinksToDom(xmlDocument=self._xmlDocument)
        self._oglUseCasesToMiniDom: OglUseCasesToDom = OglUseCasesToDom(xmlDocument=self._xmlDocument)

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

        oglClasses:     OglClasses     = cast(OglClasses, oglDocument.oglClasses)
        oglLinks:       OglLinks       = cast(OglLinks, oglDocument.oglLinks)
        oglTexts:       OglTexts       = cast(OglTexts, oglDocument.oglTexts)
        oglUseCases:    OglUseCases    = cast(OglUseCases, oglDocument.oglUseCases)
        oglActors:      OglActors      = cast(OglActors, oglDocument.oglActors)
        oglSDInstances: OglSDInstances = cast(OglSDInstances, oglDocument.oglSDInstances)
        oglSDMessages:  OglSDMessages  = cast(OglSDMessages,  oglDocument.oglSDMessages)

        documentNode = self._oglClassesToMiniDom.serialize(documentNode=documentNode, oglClasses=oglClasses)
        documentNode = self._oglUseCasesToMiniDom.serialize(documentNode=documentNode, oglUseCases=oglUseCases, oglActors=oglActors)
        documentNode = self._oglLinksToMiniDom.serialize(documentNode=documentNode, oglLinks=oglLinks)

        for oglText in oglTexts:
            textElement: Element = self._oglTextToXml(oglText, xmlDoc=self._xmlDocument)
            documentNode.appendChild(textElement)

        for oglSDInstance in oglSDInstances.values():
            sdInstanceElement: Element = self._oglSDInstanceToXml(oglSDInstance, self._xmlDocument)
            documentNode.appendChild(sdInstanceElement)

        for oglSDMessage in oglSDMessages.values():
            sdMessageElement: Element = self.oglSDMessageToXml(oglSDMessage=oglSDMessage, xmlDoc=self._xmlDocument)
            documentNode.appendChild(sdMessageElement)

    def writeXml(self, fqFileName):
        """
        Persist the XML

        Args:
            fqFileName:  The fully qualified file name
        """

        xmlText: str = self._xmlDocument.toprettyxml()
        updatedXml: str = OglToDom.setAsISOLatin(xmlText)

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
        retText: str = xmlTextToUpdate.replace(OglToDom.ORIGINAL_XML_PROLOG, OglToDom.FIXED_XML_PROLOG)
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

    def _oglSDInstanceToXml(self, oglSDInstance: OglSDInstance, xmlDoc: Document) -> Element:
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

        pyutSDMessage: PyutSDMessage = oglSDMessage.getPyutObject()
        root.appendChild(self._pyutSDMessageToXml(pyutSDMessage, xmlDoc))

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
        # eltId: int = pyutSDInstance.id
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

        eltId: int = self._idFactory.getID(pyutSDMessage)
        # eltId: int = pyutSDMessage.id
        root.setAttribute(XmlConstants.ATTR_ID, str(eltId))

        # message
        root.setAttribute(XmlConstants.ATTR_MESSAGE, pyutSDMessage.getMessage())

        # time
        srcInstance: PyutSDInstance = pyutSDMessage.getSource()
        dstInstance: PyutSDInstance = pyutSDMessage.getDestination()

        idSrc: int = self._idFactory.getID(srcInstance)
        idDst: int = self._idFactory.getID(dstInstance)

        root.setAttribute(XmlConstants.ATTR_SOURCE_TIME_LINE, str(pyutSDMessage.getSrcTime()))
        root.setAttribute(XmlConstants.ATTR_DESTINATION_TIME_LINE, str(pyutSDMessage.getDstTime()))
        root.setAttribute(XmlConstants.ATTR_SD_MESSAGE_SOURCE_ID, str(idSrc))
        root.setAttribute(XmlConstants.ATTR_SD_MESSAGE_DESTINATION_ID, str(idDst))

        return root

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
