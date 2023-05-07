
from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from ogl.OglClass import OglClass
from ogl.OglObject import OglObject

from oglio.Types import OglClasses
from oglio.toXmlV11.PyutToXml import PyutToXml

from oglio.toXmlV11.XmlConstants import XmlConstants


class OglClassToXml:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)
        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglClasses: OglClasses) -> Element:

        for oglClass in oglClasses:
            self._oglClassToXml(documentTop=documentTop, oglClass=oglClass)

        return documentTop

    def _oglClassToXml(self, documentTop: Element, oglClass: OglClass) -> Element:
        """
        Exports an OglClass to a minidom Element.

        Args:
            documentTop:     The document to append to
            oglClass:   Ogl Class to serialize

        Returns:
            The newly created `OglClass` SubElement
        """
        attributes = self._oglBaseAttributes(oglObject=oglClass)
        oglClassSubElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_CLASS, attrib=attributes)

        self._pyutToXml.pyutClassToXml(graphicElement=oglClassSubElement, pyutClass=oglClass.pyutObject)

        return oglClassSubElement

    def _oglBaseAttributes(self, oglObject: OglObject):
        """
        Saves the position and size of the OGL object in an XML node.

        Args:
            oglObject:  OGL Object
            root:      XML node to update

        Returns:
            The updated originalElement
        """
        w, h = oglObject.GetModel().GetSize()
        x, y = oglObject.GetModel().GetPosition()

        attributes = {
            XmlConstants.ATTR_WIDTH:  str(w),
            XmlConstants.ATTR_HEIGHT: str(h),
            XmlConstants.ATTR_X:      str(x),
            XmlConstants.ATTR_Y:      str(y)
        }

        return attributes
