
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglNotes
from oglio.Types import OglTexts
from oglio.Types import OglUseCases

from oglio.toXmlV10.OglToDom import OglToDom as OglToMiniDomV10

from tests.TestBase import TestBase


class TestNotesDiagram(TestBase):
    """
    """
    NOTES_DIAGRAM_FILENAME: str    = 'ManyNotes.xml'
    clsLogger:              Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestNotesDiagram.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestNotesDiagram.clsLogger

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testNotesSerialization(self):
        #
        # Get some OglNotes
        #
        self._cleanupGenerated(TestNotesDiagram.NOTES_DIAGRAM_FILENAME)

        fqFileName: str       = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestNotesDiagram.NOTES_DIAGRAM_FILENAME)
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document = untangler.documents[DocumentTitle('Many Notes')]
        #
        #  Testing starts here
        #
        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10(projectVersion=untangler.projectInformation.version,
                                                        projectCodePath=untangler.projectInformation.codePath)

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses  = cast(OglClasses, singleDocument.oglClasses)
        oglDocument.oglLinks    = cast(OglLinks, singleDocument.oglLinks)
        oglDocument.oglTexts    = cast(OglTexts, singleDocument.oglTexts)
        oglDocument.oglNotes    = cast(OglNotes, singleDocument.oglNotes)
        oglDocument.oglUseCases = cast(OglUseCases, singleDocument.oglUseCases)
        oglDocument.oglActors   = cast(OglActors, singleDocument.oglActors)

        oglToMiniDom.serialize(oglDocument=oglDocument)

        generatedFileName: str = self._constructGeneratedName(TestNotesDiagram.NOTES_DIAGRAM_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(TestNotesDiagram.NOTES_DIAGRAM_FILENAME)

        self.assertEqual(0, status, 'Diff notes diagram serialization failed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestNotesDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
