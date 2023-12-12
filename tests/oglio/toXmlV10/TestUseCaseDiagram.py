
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import UnTangler

from untanglepyut.Types import Document
from untanglepyut.Types import DocumentTitle

from untanglepyut.XmlVersion import XmlVersion

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglTexts
from oglio.Types import OglUseCases

from oglio.toXmlV10.OglToDom import OglToDom as OglToMiniDomV10

from tests.ProjectTestBase import ProjectTestBase


class TestUseCaseDiagram(ProjectTestBase):
    """
    """
    USE_CASE_DIAGRAM_FILENAME: str = 'UseCaseDiagram.xml'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testUseCaseSerialization(self):

        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestUseCaseDiagram.USE_CASE_DIAGRAM_FILENAME)

        untangler:  UnTangler = UnTangler(xmlVersion=XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document = untangler.documents[DocumentTitle('Use-Cases')]

        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10(projectVersion=untangler.projectInformation.version,
                                                        projectCodePath=untangler.projectInformation.codePath)

        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglClasses  = cast(OglClasses, singleDocument.oglClasses)
        oglDocument.oglLinks    = cast(OglLinks, singleDocument.oglLinks)
        oglDocument.oglTexts    = cast(OglTexts, singleDocument.oglTexts)
        oglDocument.oglUseCases = cast(OglUseCases, singleDocument.oglUseCases)
        oglDocument.oglActors   = cast(OglActors, singleDocument.oglActors)

        oglToMiniDom.serialize(oglDocument=oglDocument)

        generatedFileName: str = ProjectTestBase.constructGeneratedName(TestUseCaseDiagram.USE_CASE_DIAGRAM_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(TestUseCaseDiagram.USE_CASE_DIAGRAM_FILENAME)

        self.assertEqual(0, status, 'Diff use case diagram serialization failed')

        ProjectTestBase.cleanupGenerated(TestUseCaseDiagram.USE_CASE_DIAGRAM_FILENAME)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUseCaseDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
