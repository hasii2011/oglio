
from typing import Dict
from typing import cast
from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import PyutMethods
from pyutmodelv2.PyutMethod import PyutModifiers

from ogl.OglClass import OglClass

from oglio import OglVersion
from oglio.Reader import Reader

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglDocumentTitle
from oglio.Types import OglDocuments
from oglio.Types import OglLinks
from oglio.Types import OglProject
from oglio.UnsupportedFileTypeException import UnsupportedFileTypeException

from tests.ProjectTestBase import ProjectTestBase


class TestReader(ProjectTestBase):
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

        fqFileName: str        = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)
        oglProject: OglProject = self._reader.readXmlFile(fqFileName=fqFileName)

        self.assertEqual(fqFileName, oglProject.fileName, 'Where is my file name')
        expectedVersion: str = OglVersion.version
        actualVersion:   str = oglProject.version
        self.assertEqual(expectedVersion, actualVersion, 'Mismatch in support Ogl Xml versions')

    def testMultiDocumentRead(self):

        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

        oglProject:   OglProject   = self._reader.readXmlFile(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments

        self.assertEqual(2, len(oglDocuments), 'Mismatch in number of Pyut Documents that were read')

    def testCorrectNumberOfOglObjectsDocumentOne(self):

        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

        oglProject:   OglProject   = self._reader.readXmlFile(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments

        try:
            oglDocument: OglDocument = oglDocuments[TestReader.TEST_DOCUMENT_NAME_1]
            self._testDocumentContents(oglDocument=oglDocument, expectedClassCount=2, expectedLinkCount=1)
        except KeyError:
            self.assertTrue(False, f'Could not find {TestReader.TEST_DOCUMENT_NAME_1}')

    def testCorrectNumberOfOglObjectsDocumentTwo(self):

        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestReader.TEST_FILE_NAME)

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
        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'SimpleMultipleDocument.put')

        oglProject:   OglProject   = self._reader.readFile(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments

        try:
            oglDocument: OglDocument = oglDocuments[OglDocumentTitle('Diagram 1')]
            self._testDocumentContents(oglDocument=oglDocument, expectedClassCount=1, expectedLinkCount=0)
        except KeyError:
            self.assertTrue(False, f'Could not find Diagram 1')

    def testReadV11XmlFile(self):

        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'SingleClassDocumentV11.xml')

        oglProject:   OglProject   = self._reader.readXmlFile(fqFileName=fqFileName)
        oglDocuments: OglDocuments = oglProject.oglDocuments
        oglDocument:  OglDocument  = oglDocuments[OglDocumentTitle('SingleClassDiagram')]

        oglClasses: OglClasses = oglDocument.oglClasses

        self.assertEqual(1, len(oglClasses), '')

        oglClass:    OglClass   = oglClasses[0]
        pyutClass:   PyutClass  = oglClass.pyutObject
        pyutMethods: PyutMethods = pyutClass.methods

        self.assertEqual(7, len(pyutMethods), '')

        methodDict: Dict[str, PyutMethod] = {}
        for method in pyutMethods:
            pyutMethod: PyutMethod = cast(PyutMethod, method)
            methodDict[pyutMethod.name] = pyutMethod

        methodWithParameters: PyutMethod = methodDict['methodWithParameters']

        self.assertEqual(3, len(methodWithParameters.parameters), '')

        methodWithModifiers: PyutMethod = methodDict['methodWithModifiers']

        modifiers: PyutModifiers = methodWithModifiers.modifiers

        self.assertEqual(2, len(modifiers), '')

    def testReadV11PutFile(self):
        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'InheritanceV11.put')

        oglProject:   OglProject = self._reader.readFile(fqFileName=fqFileName)

        oglDocuments: OglDocuments = oglProject.oglDocuments
        oglDocument:  OglDocument  = oglDocuments[OglDocumentTitle('Class Diagram')]
        oglClasses:   OglClasses   = oglDocument.oglClasses

        self.assertEqual(2, len(oglClasses), '')

        oglLinks: OglLinks = oglDocument.oglLinks

        self.assertEqual(1, len(oglLinks), '')

    def _testDocumentContents(self, oglDocument: OglDocument, expectedClassCount: int, expectedLinkCount: int):

        oglClasses: OglClasses = oglDocument.oglClasses
        oglLinks:   OglLinks   = oglDocument.oglLinks

        self.assertEqual(expectedClassCount, len(oglClasses), f'{oglDocument.documentTitle} - Not enough OGL Classes')
        self.assertEqual(expectedLinkCount,  len(oglLinks),   f'{oglDocument.documentTitle} - Not enough OGL Links')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestReader))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
