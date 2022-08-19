
from typing import cast

from logging import Logger
from logging import getLogger

from pkg_resources import resource_filename

from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglDocument

from oglio.toXmlV10.OglToMiniDom import OglToMiniDom as OglToMiniDomV10

from tests.TestBase import TestBase


class TestOglToMiniDomV10(TestBase):
    """
    The serialization code needs pre-made OGL Objects.  So we will untangle
    XML documents and feed them to the serializer;  It should return identical XML
    """
    clsLogger: Logger = cast(Logger, None)

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

        #
        # We are going to cheat and just use the project information from the Untangled XML
        # We do not want to see/make visible a PyutProject object at this layer
        #
        # xmlDocument, topElement = self._createStarterXmlDocument(projectVersion=untangler.projectInformation.version,
        #                                                          projectCodePath=untangler.projectInformation.codePath)

        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10(projectVersion=untangler.projectInformation.version,
                                                        projectCodePath=untangler.projectInformation.codePath)

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses = singleDocument.oglClasses
        oglDocument.oglLinks   = singleDocument.oglLinks
        oglDocument.oglTexts   = singleDocument.oglTexts

        oglToMiniDom.serialize(oglDocument=oglDocument)

        oglToMiniDom.writeXml(fqFileName=f'MultiLink.xml')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglToMiniDomV10))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
