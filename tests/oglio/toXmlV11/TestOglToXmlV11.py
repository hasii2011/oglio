from typing import cast
from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.toXmlV11.OglToXml import OglToXml
from tests.TestBase import TestBase

EMPTY_DOCUMENT_FILENAME: str = 'EmptyDocument.xml'
SINGLE_CLASS_FILENAME:   str = 'SingleClassDocumentV11.xml'


class TestOglToXmlV11(TestBase):
    """
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testProjectWrapper(self):
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, EMPTY_DOCUMENT_FILENAME)

        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document  = untangler.documents[DocumentTitle('EmptyDiagram')]

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)

        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)

        self.logger.info(oglToXml.xml)

        generatedFileName: str = self._constructGeneratedName(EMPTY_DOCUMENT_FILENAME)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(EMPTY_DOCUMENT_FILENAME)

        self.assertEqual(0, status, 'Diff empty document serialization failed')


    def testSingleClassProject(self):

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, SINGLE_CLASS_FILENAME)

        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document  = untangler.documents[DocumentTitle('SingleClassDiagram')]

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses = cast(OglClasses, singleDocument.oglClasses)

        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)

        self.logger.info(oglToXml.xml)

        generatedFileName: str = self._constructGeneratedName(SINGLE_CLASS_FILENAME)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(SINGLE_CLASS_FILENAME)

        # self.assertEqual(0, status, 'Diff single document serialization failed')



def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglToXmlV11))

    return testSuite


if __name__ == '__main__':
    unitTestMain()