
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename
from untanglepyut.UnTangler import Documents
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglDocumentTitle
from oglio.Types import OglDocuments
from oglio.Types import OglLinks
from oglio.Types import OglNotes
from oglio.Types import OglProject
from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages
from oglio.Types import OglTexts
from oglio.Types import OglUseCases
from oglio.Types import createOglDocumentsFactory
from oglio.Writer import Writer
from oglio.toXmlV10.OglToDom import OglToDom
from tests.TestBase import TestBase


class TestWriter(TestBase):
    """
    Test the simplified writer interface for Pyut
    """
    MULTI_DOCUMENT_FILENAME: str = 'SimpleMultipleDocument.xml'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestWriter.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestWriter.clsLogger

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSimpleWrite(self):

        oglProject:        OglProject = self._getTestOglProject()
        generatedFileName: str        = self._constructGeneratedName(TestWriter.MULTI_DOCUMENT_FILENAME)

        writer: Writer = Writer()

        writer.writeXmlFile(oglProject=oglProject, fqFileName=generatedFileName)

    def testWriteCompressedFile(self):
        """
        Manually run pyut2xml and manually diff the files
        """
        oglProject:        OglProject = self._getTestOglProject()
        generatedFileName: str        = self._constructGeneratedName('TestCompressedProject')
        writer:            Writer     = Writer()

        writer.writeFile(oglProject=oglProject, fqFileName=generatedFileName)

    def _getTestOglProject(self) -> OglProject:
        """
        I need 2 documents with Ogl Objects
        I cheat to convert one type to the other

        Returns:  An OglProject
        """
        fqFileName: str       = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestWriter.MULTI_DOCUMENT_FILENAME)
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)
        #
        # from our test Ogl Objects create the oglProject
        #
        oglProject: OglProject = OglProject()
        oglProject.version  = OglToDom.VERSION
        oglProject.codePath = '/tmp/bogus/Ozzee.py'
        generatedFileName: str = self._constructGeneratedName(TestWriter.MULTI_DOCUMENT_FILENAME)

        oglDocuments: OglDocuments = createOglDocumentsFactory()
        untangledDocuments: Documents = untangler.documents
        for untangledDocument in untangledDocuments.values():
            oglDocument: OglDocument    = OglDocument()
            oglDocument.documentType    = untangledDocument.documentType
            oglDocument.documentTitle   = OglDocumentTitle(untangledDocument.documentTitle)
            oglDocument.scrollPositionX = untangledDocument.scrollPositionX
            oglDocument.scrollPositionY = untangledDocument.scrollPositionY
            oglDocument.pixelsPerUnitX  = untangledDocument.pixelsPerUnitX
            oglDocument.pixelsPerUnitY  = untangledDocument.pixelsPerUnitY
            oglDocument.oglClasses      = cast(OglClasses, untangledDocument.oglClasses)
            oglDocument.oglLinks        = cast(OglLinks, untangledDocument.oglLinks)
            oglDocument.oglNotes        = cast(OglNotes, untangledDocument.oglNotes)
            oglDocument.oglTexts        = cast(OglTexts, untangledDocument.oglTexts)
            oglDocument.oglActors       = cast(OglActors, untangledDocument.oglActors)
            oglDocument.oglUseCases     = cast(OglUseCases, untangledDocument.oglUseCases)
            oglDocument.oglSDInstances  = cast(OglSDInstances, untangledDocument.oglSDInstances)
            oglDocument.oglSDMessages   = cast(OglSDMessages, untangledDocument.oglSDMessages)

            oglDocuments[oglDocument.documentTitle] = oglDocument

        oglProject.oglDocuments = oglDocuments

        return oglProject


def suite() -> TestSuite:
    """
    """
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestWriter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
