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
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, EMPTY_DOCUMENT_FILENAME)

        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document  = untangler.documents[DocumentTitle('EmptyDiagram')]

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)

        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)

        self.logger.debug(oglToXml.xml)

        generatedFileName: str = TestBase.constructGeneratedName(EMPTY_DOCUMENT_FILENAME)

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

        generatedFileName: str = TestBase.constructGeneratedName(SINGLE_CLASS_FILENAME_V11)

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

        generatedFileName: str = TestBase.constructGeneratedName(MULTI_LINK_FILE_NAME_V11)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(MULTI_LINK_FILE_NAME_V11)

        self.assertEqual(0, status, 'Diff multi link document serialization failed')

    def testControlPoints(self):
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, CRAZY_CONTROL_POINTS_V10)

        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document  = untangler.documents[DocumentTitle('CrazyAssociation')]

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses = cast(OglClasses, singleDocument.oglClasses)
        oglDocument.oglLinks   = cast(OglLinks,   singleDocument.oglLinks)

        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)

        self.logger.debug(oglToXml.xml)

        generatedFileName: str = TestBase.constructGeneratedName(CRAZY_CONTROL_POINTS_V11)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(CRAZY_CONTROL_POINTS_V11)

        self.assertEqual(0, status, 'Diff multi link document serialization failed')

    def testSplines(self):
        oglDocument: OglDocument = self._getOglDocument(baseFileName=WACKY_SPLINES_V10, documentName='WackySpline')
        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)

        self.logger.debug(oglToXml.xml)
        generatedFileName: str = TestBase.constructGeneratedName(WACKY_SPLINES_V11)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(WACKY_SPLINES_V11)

        self.assertEqual(0, status, 'Diff spline serialization failed')

    def testTextAndLinkedNotes(self):
        oglDocument: OglDocument = self._getOglDocument(baseFileName=TEXT_AND_LINKED_NOTES_V10, documentName='TextNotes')
        oglToXml: OglToXml = OglToXml(projectCodePath='')
        oglToXml.serialize(oglDocument)

        self.logger.debug(oglToXml.xml)
        generatedFileName: str = TestBase.constructGeneratedName(TEXT_AND_LINKED_NOTES_V11)

        oglToXml.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(TEXT_AND_LINKED_NOTES_V11)

        self.assertEqual(0, status, 'Diff multi link document serialization failed')


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
