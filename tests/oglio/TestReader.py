
from unittest import TestSuite
from unittest import main as unitTestMain

from oglio import OglVersion
from oglio.Reader import Reader

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglDocumentTitle
from oglio.Types import OglDocuments
from oglio.Types import OglLinks
from oglio.Types import OglProject
from oglio.UnsupportedFileTypeException import UnsupportedFileTypeException

from tests.TestBase import TestBase


class TestReader(TestBase):
    """
    """
    TEST_FILE_NAME:       str = 'MultiDocumentProject.xml'
    TEST_DOCUMENT_NAME_1: OglDocumentTitle = OglDocumentTitle('Diagram-1')
    TEST_DOCUMENT_NAME_2: OglDocumentTitle = OglDocumentTitle('Diagram-2')

    def setUp(self):
        super().setUp()
        self._reader: Reader = Reader()

    def tearDown(self):
        super().tearDown()

    def testProjectInformation(self):

        fqFileName: str        = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)
        oglProject: OglProject = self._reader.readXmlFile(fqFileName=fqFileName)

        self.assertEqual(fqFileName, oglProject.fileName, 'Where is my file name')
        expectedVersion: str = OglVersion.version
        actualVersion:   str = oglProject.version
        self.assertEqual(expectedVersion, actualVersion, 'Mismatch in support Ogl Xml versions')

    def testMultiDocumentRead(self):

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

        oglProject:   OglProject   = self._reader.readXmlFile(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments

        self.assertEqual(2, len(oglDocuments), 'Mismatch in number of Pyut Documents that were read')

    def testCorrectNumberOfOglObjectsDocumentOne(self):

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

        oglProject:   OglProject   = self._reader.readXmlFile(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments

        try:
            oglDocument: OglDocument = oglDocuments[TestReader.TEST_DOCUMENT_NAME_1]
            self._testDocumentContents(oglDocument=oglDocument, expectedClassCount=2, expectedLinkCount=1)
        except KeyError:
            self.assertTrue(False, f'Could not find {TestReader.TEST_DOCUMENT_NAME_1}')

    def testCorrectNumberOfOglObjectsDocumentTwo(self):

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

        oglProject: OglProject = self._reader.readXmlFile(fqFileName=fqFileName)

        oglDocuments: OglDocuments = oglProject.oglDocuments

        try:
            oglDocument: OglDocument = oglDocuments[TestReader.TEST_DOCUMENT_NAME_2]
            self._testDocumentContents(oglDocument=oglDocument, expectedClassCount=7, expectedLinkCount=4)
        except KeyError:
            self.assertTrue(False, f'Could not find {TestReader.TEST_DOCUMENT_NAME_2}')

    def testIncorrectXmlSuffix(self):
        self.assertRaises(UnsupportedFileTypeException, self._reader.readXmlFile, 'HokeyXmlFileName.opie')

    def testIncorrectPutSuffix(self):
        self.assertRaises(UnsupportedFileTypeException, self._reader.readXmlFile, 'HokeyPutFileName.ozzee')

    def testReadCompressedFile(self):
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'SimpleMultipleDocument.put')

        oglProject:   OglProject   = self._reader.readFile(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments

        try:
            oglDocument: OglDocument = oglDocuments[OglDocumentTitle('Diagram 1')]
            self._testDocumentContents(oglDocument=oglDocument, expectedClassCount=1, expectedLinkCount=0)
        except KeyError:
            self.assertTrue(False, f'Could not find Diagram 1')

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
