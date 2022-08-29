
from typing import cast

from logging import Logger
from logging import getLogger

from pkg_resources import resource_filename

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodel.PyutObject import PyutObject
from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglDocument
from oglio.toXmlV10.BaseToDom import IDFactory

from oglio.toXmlV10.OglToDom import OglToDom as OglToMiniDomV10

from tests.TestBase import TestBase


class TestUseCaseDiagram(TestBase):
    """
    """
    USE_CASE_DIAGRAM_FILENAME: str = 'UseCaseDiagram.xml'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestUseCaseDiagram.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestUseCaseDiagram.clsLogger

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testUseCaseSerialization(self):

        self._cleanupGenerated(TestUseCaseDiagram.USE_CASE_DIAGRAM_FILENAME)

        fqFileName: str       = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestUseCaseDiagram.USE_CASE_DIAGRAM_FILENAME)
        untangler:  UnTangler = UnTangler(fqFileName=fqFileName)

        untangler.untangle()

        singleDocument: Document = untangler.documents['Use-Cases']

        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10(projectVersion=untangler.projectInformation.version,
                                                        projectCodePath=untangler.projectInformation.codePath)

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses  = singleDocument.oglClasses
        oglDocument.oglLinks    = singleDocument.oglLinks
        oglDocument.oglTexts    = singleDocument.oglTexts
        oglDocument.oglUseCases = singleDocument.oglUseCases
        oglDocument.oglActors   = singleDocument.oglActors

        oglToMiniDom.serialize(oglDocument=oglDocument)

        generatedFileName: str = self._constructGeneratedName(TestUseCaseDiagram.USE_CASE_DIAGRAM_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(TestUseCaseDiagram.USE_CASE_DIAGRAM_FILENAME)

        self.assertEqual(0, status, 'Diff use case diagram serialization failed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUseCaseDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
