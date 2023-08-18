
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from untanglepyut.v10.UnTangler import UnTangler

from untanglepyut.Types import Document
from untanglepyut.Types import DocumentTitle

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

    def setUp(self):
        super().setUp()
        self._mockDC: MagicMock = MagicMock()

    def tearDown(self):
        super().tearDown()

    def testNotesSerialization(self):
        #
        # Get some OglNotes
        #
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestNotesDiagram.NOTES_DIAGRAM_FILENAME)

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

        generatedFileName: str = TestBase.constructGeneratedName(TestNotesDiagram.NOTES_DIAGRAM_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(TestNotesDiagram.NOTES_DIAGRAM_FILENAME)

        self.assertEqual(0, status, 'Diff notes diagram serialization failed')

        TestBase.cleanupGenerated(TestNotesDiagram.NOTES_DIAGRAM_FILENAME)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestNotesDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
