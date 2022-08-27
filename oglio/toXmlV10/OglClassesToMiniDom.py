
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from ogl.OglClass import OglClass

from pyutmodel.PyutClass import PyutClass

from oglio.Types import OglClasses

from oglio.toXmlV10.BaseOglToDom import BaseOglToDom
from oglio.toXmlV10.PyutToDom import PyutToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglClassesToMiniDom(BaseOglToDom):

    def __init__(self, xmlDocument: Document):

        super().__init__(xmlDocument=xmlDocument)
        self.logger: Logger = getLogger(__name__)

        self._pyutToMiniDom: PyutToDom = PyutToDom()

    def serialize(self, documentNode: Element, oglClasses: OglClasses) -> Element:

        for oglClass in oglClasses:
            classElement: Element = self._oglClassToXml(oglClass=oglClass, xmlDoc=self._xmlDocument)
            documentNode.appendChild(classElement)

        return documentNode

    def _oglClassToXml(self, oglClass: OglClass, xmlDoc: Document) -> Element:
        """
        Exports an OglClass to a minidom Element.

        Args:
            oglClass:   Graphic Class to save
            xmlDoc:     The document to append to

        Returns:
            The newly created `GraphicClass` element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_CLASS)

        root = self._appendOglBase(oglClass, root)

        # adding the data layer object
        root.appendChild(self._pyutToMiniDom.pyutClassToXml(cast(PyutClass, oglClass.pyutObject), xmlDoc))

        return root
