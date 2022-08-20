
from xml.dom.minidom import Element

from pyutmodel.PyutClassCommon import PyutClassCommon

from oglio.toXmlV10.BaseToMiniDom import BaseToMiniDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class BasePyutToMiniDom(BaseToMiniDom):

    def __init__(self):
        super().__init__()

    def _pyutClassCommonToXml(self, classCommon: PyutClassCommon, root: Element) -> Element:

        root.setAttribute(XmlConstants.ATTR_DESCRIPTION, classCommon.description)
        # root.setAttribute(PyutXmlConstants.ATTR_FILENAME,    pyutInterface.getFilename())

        return root
