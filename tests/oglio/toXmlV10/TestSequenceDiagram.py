
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename
from untanglepyut.UnTangler import Document

from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglDocument

from oglio.toXmlV10.OglToDom import OglToDom as OglToMiniDomV10

from tests.TestBase import TestBase


class TestSequenceDiagram(TestBase):
    """
    """
    SEQUENCE_DIAGRAM_FILENAME: str = 'SimpleSequenceDiagram.xml'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestSequenceDiagram.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestSequenceDiagram.clsLogger

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSequenceDiagramSerialization(self):

        self._cleanupGenerated(TestSequenceDiagram.SEQUENCE_DIAGRAM_FILENAME)

        fqFileName: str       = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestSequenceDiagram.SEQUENCE_DIAGRAM_FILENAME)
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document = untangler.documents['SimpleSequence']

        # we now have ogl objects to serialize

        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10(projectVersion=untangler.projectInformation.version,
                                                        projectCodePath=untangler.projectInformation.codePath)
        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglSDInstances = singleDocument.oglSDInstances
        oglDocument.oglSDMessages  = singleDocument.oglSDMessages

        oglToMiniDom.serialize(oglDocument=oglDocument)

        generatedFileName: str = self._constructGeneratedName(TestSequenceDiagram.SEQUENCE_DIAGRAM_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(TestSequenceDiagram.SEQUENCE_DIAGRAM_FILENAME)

        self.assertEqual(0, status, 'Diff of sequence diagram serialization failed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestSequenceDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
