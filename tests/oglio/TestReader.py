
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from oglio.Reader import Reader

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglDocuments
from oglio.Types import OglLinks
from oglio.Types import OglProject

from tests.TestBase import TestBase


class TestReader(TestBase):
    """
    """
    TEST_FILE_NAME:       str = 'MultiDocumentProject.xml'
    TEST_DOCUMENT_NAME_1: str = 'Diagram-1'
    TEST_DOCUMENT_NAME_2: str = 'Diagram-2'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestReader.clsLogger = getLogger(__name__)

    def setUp(self):
        super().setUp()
        self.logger:  Logger = TestReader.clsLogger
        self._reader: Reader = Reader()

    def tearDown(self):
        super().tearDown()

    def testMultiDocumentRead(self):

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

        oglProject:   OglProject   = self._reader.read(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments

        self.assertEqual(2, len(oglDocuments), 'Mismatch in number of Pyut Documents that were read')

    def testCorrectNumberOfOglObjectsDocumentOne(self):

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

        oglProject:   OglProject   = self._reader.read(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments

        try:
            oglDocument: OglDocument = oglDocuments[TestReader.TEST_DOCUMENT_NAME_1]
            self._testDocumentContents(oglDocument=oglDocument, expectedClassCount=2, expectedLinkCount=1)
        except KeyError:
            self.assertTrue(False, f'Could not find {TestReader.TEST_DOCUMENT_NAME_1}')

    def testCorrectNumberOfOglObjectsDocumentTwo(self):

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

        oglProject: OglProject = self._reader.read(fqFileName=fqFileName)

        oglDocuments: OglDocuments = oglProject.oglDocuments

        try:
            oglDocument: OglDocument = oglDocuments[TestReader.TEST_DOCUMENT_NAME_2]
            self._testDocumentContents(oglDocument=oglDocument, expectedClassCount=7, expectedLinkCount=4)
        except KeyError:
            self.assertTrue(False, f'Could not find {TestReader.TEST_DOCUMENT_NAME_2}')

    def _testDocumentContents(self, oglDocument: OglDocument, expectedClassCount: int, expectedLinkCount: int):

        oglClasses: OglClasses = oglDocument.oglClasses
        oglLinks:   OglLinks   = oglDocument.oglLinks

        self.assertEqual(expectedClassCount, len(oglClasses), f'{oglDocument.documentTitle} - Not enough OGL Classes')
        self.assertEqual(expectedLinkCount,  len(oglLinks),   f'{oglDocument.documentTitle} - Not enough OGL Links')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestReader))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
