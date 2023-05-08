from typing import cast
from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.toXmlV11.OglToXml import OglToXml
from tests.TestBase import TestBase

EMPTY_DOCUMENT_FILENAME:     str = 'EmptyDocument.xml'
SINGLE_CLASS_FILENAME_V10:   str = 'SingleClassDocumentV10.xml'
SINGLE_CLASS_FILENAME_V11:   str = 'SingleClassDocumentV11.xml'

MULTI_LINK_FILE_NAME_V10:    str = 'MultiLinkDocumentV10.xml'
MULTI_LINK_FILE_NAME_V11:    str = 'MultiLinkDocumentV11.xml'

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

        self.logger.debug(oglToXml.xml)

        generatedFileName: str = self._constructGeneratedName(EMPTY_DOCUMENT_FILENAME)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(EMPTY_DOCUMENT_FILENAME)

        self.assertEqual(0, status, 'Diff empty document serialization failed')

    def testSingleClassProject(self):

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, SINGLE_CLASS_FILENAME_V10)

        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document  = untangler.documents[DocumentTitle('SingleClassDiagram')]

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses = cast(OglClasses, singleDocument.oglClasses)

        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)

        self.logger.debug(oglToXml.xml)

        generatedFileName: str = self._constructGeneratedName(SINGLE_CLASS_FILENAME_V11)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(SINGLE_CLASS_FILENAME_V11)

        self.assertEqual(0, status, 'Diff single document serialization failed')

    def testMultipleLinks(self):

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, MULTI_LINK_FILE_NAME_V10)

        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document  = untangler.documents[DocumentTitle('MultiLink')]

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses = cast(OglClasses, singleDocument.oglClasses)
        oglDocument.oglLinks   = cast(OglLinks,   singleDocument.oglLinks)

        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)
        self.logger.debug(oglToXml.xml)

        generatedFileName: str = self._constructGeneratedName(MULTI_LINK_FILE_NAME_V11)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(MULTI_LINK_FILE_NAME_V11)

        self.assertEqual(0, status, 'Diff multi link document serialization failed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglToXmlV11))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
