from typing import cast
from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglNotes
from oglio.Types import OglTexts
from oglio.toXmlV11.OglToXml import OglToXml
from tests.TestBase import TestBase

EMPTY_DOCUMENT_FILENAME:     str = 'EmptyDocument.xml'
SINGLE_CLASS_FILENAME_V10:   str = 'SingleClassDocumentV10.xml'
SINGLE_CLASS_FILENAME_V11:   str = 'SingleClassDocumentV11.xml'

MULTI_LINK_FILE_NAME_V10:    str = 'MultiLinkDocumentV10.xml'
MULTI_LINK_FILE_NAME_V11:    str = 'MultiLinkDocumentV11.xml'

CRAZY_CONTROL_POINTS_V10:    str = 'CrazyControlPointsV10.xml'
CRAZY_CONTROL_POINTS_V11:    str = 'CrazyControlPointsV11.xml'

WACKY_SPLINES_V10: str = 'WackySplinesV10.xml'
WACKY_SPLINES_V11: str = 'WackySplinesV11.xml'

TEXT_AND_LINKED_NOTES_V10: str = 'TextAndLinkedNotesV10.xml'
TEXT_AND_LINKED_NOTES_V11: str = 'TextAndLinkedNotesV11.xml'

GENERATED_FILE_NAMES = [EMPTY_DOCUMENT_FILENAME, SINGLE_CLASS_FILENAME_V11, MULTI_LINK_FILE_NAME_V11, CRAZY_CONTROL_POINTS_V11, WACKY_SPLINES_V11, TEXT_AND_LINKED_NOTES_V11]

class TestOglToXmlV11(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.clsLogger.warning(f'tearDownClass {cls.keep=}')
        if cls.keep is False:
            for fileName in GENERATED_FILE_NAMES:
                cls.cleanupGenerated(fileName=fileName)

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testProjectWrapper(self):
        oglDocument: OglDocument = self._getOglDocument(baseFileName=EMPTY_DOCUMENT_FILENAME, documentName='EmptyDiagram')
        self._assertGeneratedFile(oglDocument=oglDocument, baseFileNameV11=EMPTY_DOCUMENT_FILENAME,  assertionMessage='Diff empty document serialization failed')

    def testSingleClassProject(self):
        oglDocument: OglDocument = self._getOglDocument(baseFileName=SINGLE_CLASS_FILENAME_V10, documentName='SingleClassDiagram')
        self._assertGeneratedFile(oglDocument=oglDocument, baseFileNameV11=SINGLE_CLASS_FILENAME_V11, assertionMessage='Diff single document serialization failed')

    def testMultipleLinks(self):
        oglDocument: OglDocument = self._getOglDocument(baseFileName=MULTI_LINK_FILE_NAME_V10, documentName='MultiLink')
        self._assertGeneratedFile(oglDocument=oglDocument, baseFileNameV11=MULTI_LINK_FILE_NAME_V11, assertionMessage='Diff multi link document serialization failed')

    def testControlPoints(self):
        oglDocument: OglDocument = self._getOglDocument(baseFileName=CRAZY_CONTROL_POINTS_V10, documentName='CrazyAssociation')
        self._assertGeneratedFile(oglDocument=oglDocument, baseFileNameV11=CRAZY_CONTROL_POINTS_V11, assertionMessage='Diff multi link document serialization failed')

    def testSplines(self):
        oglDocument: OglDocument = self._getOglDocument(baseFileName=WACKY_SPLINES_V10, documentName='WackySpline')
        self._assertGeneratedFile(oglDocument=oglDocument, baseFileNameV11=WACKY_SPLINES_V11, assertionMessage='Diff spline serialization failed')

    def testTextAndLinkedNotes(self):
        oglDocument: OglDocument = self._getOglDocument(baseFileName=TEXT_AND_LINKED_NOTES_V10, documentName='TextNotes')
        self._assertGeneratedFile(oglDocument=oglDocument, baseFileNameV11=TEXT_AND_LINKED_NOTES_V11, assertionMessage='Diff multi link document serialization failed')

    def _assertGeneratedFile(self, oglDocument: OglDocument, baseFileNameV11: str, assertionMessage: str):

        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)
        self.logger.debug(oglToXml.xml)

        generatedFileName: str = TestBase.constructGeneratedName(baseFileNameV11)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(baseFileNameV11)

        self.assertEqual(0, status, assertionMessage)

    def _getOglDocument(self, baseFileName: str, documentName: str) -> OglDocument:

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, baseFileName)

        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document  = untangler.documents[DocumentTitle(documentName)]

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses = cast(OglClasses, singleDocument.oglClasses)
        oglDocument.oglLinks   = cast(OglLinks,   singleDocument.oglLinks)
        oglDocument.oglNotes   = cast(OglNotes,   singleDocument.oglNotes)
        oglDocument.oglTexts   = cast(OglTexts,   singleDocument.oglTexts)
        # TODO Copy the rest

        return oglDocument

def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglToXmlV11))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
