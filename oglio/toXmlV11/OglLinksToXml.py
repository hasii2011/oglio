
from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from ogl.OglAssociation import OglAssociation
from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink

from oglio.Types import OglLinks

from oglio.toXmlV11.PyutToXml import PyutToXml
from oglio.toXmlV11.XmlConstants import XmlConstants
from oglio.toXmlV11.BaseOglToXml import BaseOglToXml
from oglio.toXmlV11.InternalTypes import ElementAttributes


class OglLinksToXml(BaseOglToXml):
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglLinks: OglLinks) -> Element:

        for oglLink in oglLinks:
            if isinstance(oglLink, OglInterface2):
                pass        # TODO
            else:
                self._oglLinkToXml(documentTop=documentTop, oglLink=oglLink)

        return documentTop

    def _oglLinkToXml(self, documentTop: Element, oglLink: OglLink) -> Element:

        attributes:        ElementAttributes = self._oglLinkAttributes(oglLink=oglLink)
        oglLinkSubElement: Element           = SubElement(documentTop, XmlConstants.ELEMENT_OGL_LINK, attrib=attributes)

        if isinstance(oglLink, OglAssociation):

            center: OglAssociationLabel = oglLink.centerLabel
            src:    OglAssociationLabel = oglLink.sourceCardinality
            dst:    OglAssociationLabel = oglLink.destinationCardinality
            associationLabels = {
                XmlConstants.ELEMENT_ASSOCIATION_CENTER_LABEL:      center,
                XmlConstants.ELEMENT_ASSOCIATION_SOURCE_LABEL:      src,
                XmlConstants.ELEMENT_ASSOCIATION_DESTINATION_LABEL: dst
            }
            for eltName in associationLabels:
                oglLabel: OglAssociationLabel = associationLabels[eltName]
                x: int = oglLabel.oglPosition.x
                y: int = oglLabel.oglPosition.y

                labelAttributes: ElementAttributes = ElementAttributes({
                    XmlConstants.ATTR_X: str(x),
                    XmlConstants.ATTR_Y: str(y),
                })
                # noinspection PyUnusedLocal
                labelElement: Element = SubElement(oglLinkSubElement, eltName, attrib=labelAttributes)

        # save control points (not anchors!)
        for x, y in oglLink.segments[1:-1]:
            controlPointAttributes: ElementAttributes = ElementAttributes({
                XmlConstants.ATTR_X: str(x),
                XmlConstants.ATTR_Y: str(y),
            })
            SubElement(oglLinkSubElement, XmlConstants.ELEMENT_MODEL_CONTROL_POINT, attrib=controlPointAttributes)

        self._pyutToXml.pyutLinkToXml(pyutLink=oglLink.pyutObject, oglLinkElement=oglLinkSubElement)

        return oglLinkSubElement

    def _oglLinkAttributes(self, oglLink: OglLink) -> ElementAttributes:

        srcX, srcY   = oglLink.sourceAnchor.GetModel().GetPosition()
        destX, destY = oglLink.destinationAnchor.GetModel().GetPosition()

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_LINK_SOURCE_ANCHOR_X:      str(srcX),
            XmlConstants.ATTR_LINK_SOURCE_ANCHOR_Y:      str(srcY),
            XmlConstants.ATTR_LINK_DESTINATION_ANCHOR_X: str(destX),
            XmlConstants.ATTR_LINK_DESTINATION_ANCHOR_Y: str(destY),
            XmlConstants.ATTR_SPLINE:                    str(oglLink.GetSpline())   # piecewise polynomial function
        })

        return attributes