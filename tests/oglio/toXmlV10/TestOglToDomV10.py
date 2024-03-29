
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodelv2.PyutObject import PyutObject
from pyutmodelv2.PyutObject import infiniteSequence

from untanglepyut.UnTangler import UnTangler

from untanglepyut.Types import DocumentTitle
from untanglepyut.Types import Document

from untanglepyut.XmlVersion import XmlVersion

from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglTexts


from oglio.toXmlV10.OglToDom import OglToDom as OglToMiniDomV10

from tests.ProjectTestBase import ProjectTestBase

MULTI_LINK_DOCUMENT_FILENAME: str = 'MultiLinkDocumentV10.xml'


class TestOglToDomV10(ProjectTestBase):
    """
    The serialization code needs pre-made OGL Objects.  So we will untangle
    XML documents and feed them to the serializer;  It should return identical XML
    """
    def setUp(self):
        super().setUp()

        PyutObject.idGenerator = infiniteSequence()
        next(PyutObject.idGenerator)

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
        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, MULTI_LINK_DOCUMENT_FILENAME)

        untangler:  UnTangler = UnTangler(xmlVersion=XmlVersion.V10)

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

        generatedFileName: str = ProjectTestBase.constructGeneratedName(MULTI_LINK_DOCUMENT_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(MULTI_LINK_DOCUMENT_FILENAME)

        self.assertEqual(0, status, 'Diff simple class serialization failed')

        ProjectTestBase.cleanupGenerated(MULTI_LINK_DOCUMENT_FILENAME)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOglToDomV10))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
