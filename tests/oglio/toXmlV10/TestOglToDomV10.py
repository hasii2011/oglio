
from typing import cast

from logging import Logger
from logging import getLogger

from pkg_resources import resource_filename

from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglDocument

from oglio.toXmlV10.OglToDom import OglToDom as OglToMiniDomV10

from tests.TestBase import TestBase

MULTI_LINK_DOCUMENT_FILENAME: str = 'MultiLinkDocument.xml'


class TestOglToDomV10(TestBase):
    """
    The serialization code needs pre-made OGL Objects.  So we will untangle
    XML documents and feed them to the serializer;  It should return identical XML
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglToDomV10.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglToDomV10.clsLogger

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSimpleSerialization(self):

        fqFileName = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, MULTI_LINK_DOCUMENT_FILENAME)

        untangler: UnTangler = UnTangler(fqFileName=fqFileName)

        untangler.untangle()

        singleDocument: Document          = untangler.documents['MultiLink']

        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10(projectVersion=untangler.projectInformation.version,
                                                        projectCodePath=untangler.projectInformation.codePath)

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses = singleDocument.oglClasses
        oglDocument.oglLinks   = singleDocument.oglLinks
        oglDocument.oglTexts   = singleDocument.oglTexts

        oglToMiniDom.serialize(oglDocument=oglDocument)

        generatedFileName: str = self._constructGeneratedName(MULTI_LINK_DOCUMENT_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(MULTI_LINK_DOCUMENT_FILENAME)

        self.assertEqual(0, status, 'Diff simple class serialization failed')
        self._cleanupGenerated(MULTI_LINK_DOCUMENT_FILENAME)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglToDomV10))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
