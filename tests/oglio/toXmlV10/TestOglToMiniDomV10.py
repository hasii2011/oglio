from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglInterface2 import OglInterface2
from pkg_resources import resource_filename

from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import UnTangler

from xml.dom.minidom import Document as XmlDocument
from xml.dom.minidom import Element as XmlElement

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglTexts

from oglio.toXmlV10.OglToMiniDom import OglToMiniDom as OglToMiniDomV10

from oglio.toXmlV10.XmlConstants import XmlConstants

from tests.TestBase import TestBase


class TestOglToMiniDomV10(TestBase):
    """
    The serialization code needs pre-made OGL Objects.  So we will untangle
    XML documents and feed them to the serializer;  It should return identical XML
    """
    ORIGINAL_XML_PROLOG: str = '<?xml version="1.0" ?>'
    FIXED_XML_PROLOG:    str = '<?xml version="1.0" encoding="iso-8859-1"?>'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setAsISOLatin(cls, xmlTextToUpdate: str) -> str:
        """
        Add attribute encoding = "iso-8859-1" this is not possible with minidom, so we use pattern matching

        Args:
            xmlTextToUpdate:  Old XML

        Returns:  Updated XML
        """
        retText: str = xmlTextToUpdate.replace(TestOglToMiniDomV10.ORIGINAL_XML_PROLOG, TestOglToMiniDomV10.FIXED_XML_PROLOG)
        return retText

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglToMiniDomV10.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglToMiniDomV10.clsLogger

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSimpleSerialization(self):

        fqFileName = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'MultiLinkDocument.xml')

        untangler: UnTangler = UnTangler(fqFileName=fqFileName)

        untangler.untangle()

        singleDocument: Document          = untangler.documents['MultiLink']

        xmlDocument, topElement = self._createStarterXmlDocument(projectVersion=untangler.projectInformation.version,
                                                                 projectCodePath=untangler.projectInformation.codePath)
        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        documentNode: XmlElement = self._oglDocumentToXml(xmlDoc=xmlDocument, oglDocument=oglDocument)

        topElement.appendChild(documentNode)
        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10()
        oglClasses: OglClasses = cast(OglClasses, singleDocument.oglClasses)
        for oglClass in oglClasses:
            classElement: XmlElement = oglToMiniDom.oglClassToXml(oglClass=oglClass, xmlDoc=xmlDocument)
            documentNode.appendChild(classElement)

        oglLinks: OglLinks = cast(OglLinks, singleDocument.oglLinks)
        for oglLink in oglLinks:
            if isinstance(oglLink, OglInterface2):
                lollipopElement: XmlElement = oglToMiniDom.oglInterface2ToXml(oglLink, xmlDocument)
                documentNode.appendChild(lollipopElement)
            else:
                linkElement: XmlElement = oglToMiniDom.oglLinkToXml(oglLink=oglLink, xmlDoc=xmlDocument)
                documentNode.appendChild(linkElement)

        oglTexts: OglTexts = cast(OglTexts, singleDocument.oglTexts)
        for oglText in oglTexts:
            textElement: XmlElement = oglToMiniDom.oglTextToXml(oglText, xmlDoc=xmlDocument)
            documentNode.appendChild(textElement)

        self._writeXml(xmlDocument=xmlDocument)

    def _createStarterXmlDocument(self, projectVersion: str, projectCodePath: str) -> Tuple[XmlDocument, XmlElement]:

        xmlDocument: XmlDocument = XmlDocument()
        #
        # We are going to cheat and just use the project information from the Untangled XML
        # We do not want to see/make visible a PyutProject object at this layer
        #
        topElement: XmlElement = xmlDocument.createElement(XmlConstants.TOP_LEVEL_ELEMENT)

        topElement.setAttribute(XmlConstants.ATTR_VERSION, projectVersion)
        topElement.setAttribute(XmlConstants.ATTR_CODE_PATH, projectCodePath)

        xmlDocument.appendChild(topElement)

        return xmlDocument, topElement

    def _oglDocumentToXml(self, xmlDoc: XmlDocument, oglDocument: OglDocument) -> XmlElement:

        documentNode = xmlDoc.createElement(XmlConstants.ELEMENT_DOCUMENT)

        documentNode.setAttribute(XmlConstants.ATTR_TYPE, oglDocument.documentType)
        documentNode.setAttribute(XmlConstants.ATTR_TITLE, oglDocument.documentTitle)

        documentNode.setAttribute(XmlConstants.ATTR_SCROLL_POSITION_X, str(oglDocument.scrollPositionX))
        documentNode.setAttribute(XmlConstants.ATTR_SCROLL_POSITION_Y, str(oglDocument.scrollPositionY))

        documentNode.setAttribute(XmlConstants.ATTR_PIXELS_PER_UNIT_X, str(oglDocument.pixelsPerUnitX))
        documentNode.setAttribute(XmlConstants.ATTR_PIXELS_PER_UNIT_Y, str(oglDocument.pixelsPerUnitY))

        return documentNode

    def _writeXml(self, xmlDocument: XmlDocument):

        xmlText: str = xmlDocument.toprettyxml()
        updatedXml: str = TestOglToMiniDomV10.setAsISOLatin(xmlText)

        with open('generated.xml', 'w') as fd:
            fd.write(updatedXml)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglToMiniDomV10))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
