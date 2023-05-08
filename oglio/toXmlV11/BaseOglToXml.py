
from logging import Logger
from logging import getLogger

from ogl.OglObject import OglObject

from oglio.IDFactory import IDFactory

from oglio.toXmlV10.XmlConstants import XmlConstants


class BaseOglToXml:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def _oglBaseAttributes(self, oglObject: OglObject):
        """
        Create the common OglObject attributes

        Args:
            oglObject:  OGL Object

        Returns:
            The updated originalElement
        """
        w, h = oglObject.GetModel().GetSize()
        x, y = oglObject.GetModel().GetPosition()

        attributes = {
            XmlConstants.ATTR_WIDTH:  str(w),
            XmlConstants.ATTR_HEIGHT: str(h),
            XmlConstants.ATTR_X:      str(x),
            XmlConstants.ATTR_Y:      str(y),
        }

        return attributes
