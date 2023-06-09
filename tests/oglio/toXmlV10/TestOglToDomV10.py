
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodel.PyutObject import PyutObject

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglTexts

from oglio.toXmlV10.BaseToDom import IDFactory

from oglio.toXmlV10.OglToDom import OglToDom as OglToMiniDomV10

from tests.TestBase import TestBase

MULTI_LINK_DOCUMENT_FILENAME: str = 'MultiLinkDocumentV10.xml'


class TestOglToDomV10(TestBase):
    """
    The serialization code needs pre-made OGL Objects.  So we will untangle
    XML documents and feed them to the serializer;  It should return identical XML
    """
    def setUp(self):
        super().setUp()

        PyutObject.nextId = 0   # reset to match sequence diagram
        IDFactory.nextID = 1

    def tearDown(self):
        super().tearDown()

    def testSimpleSerialization(self):
        """
        TODO:  This test is sensitive to the ogl preferences for text
            text_bold = False
            text_italicize = False
            text_font_family = Swiss
            text_font_size = 14
        Save the current preferences;  Set these;  then at test conclusion restore them
        """
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, MULTI_LINK_DOCUMENT_FILENAME)

        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document          = untangler.documents[DocumentTitle('MultiLink')]

        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10(projectVersion=untangler.projectInformation.version,
                                                        projectCodePath=untangler.projectInformation.codePath)

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses = cast(OglClasses, singleDocument.oglClasses)
        oglDocument.oglLinks   = cast(OglLinks, singleDocument.oglLinks)
        oglDocument.oglTexts   = cast(OglTexts, singleDocument.oglTexts)

        oglToMiniDom.serialize(oglDocument=oglDocument)

        generatedFileName: str = TestBase.constructGeneratedName(MULTI_LINK_DOCUMENT_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(MULTI_LINK_DOCUMENT_FILENAME)

        self.assertEqual(0, status, 'Diff simple class serialization failed')

        TestBase.cleanupGenerated(MULTI_LINK_DOCUMENT_FILENAME)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOglToDomV10))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
