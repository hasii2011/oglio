
from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import UnTangler

from untanglepyut.Types import Document
from untanglepyut.Types import DocumentTitle

from untanglepyut.XmlVersion import XmlVersion

from oglio.Types import OglDocument
from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages

from oglio.toXmlV10.OglToDom import OglToDom as OglToMiniDomV10

from tests.ProjectTestBase import ProjectTestBase


class TestSequenceDiagram(ProjectTestBase):
    """
    """
    SEQUENCE_DIAGRAM_FILENAME: str = 'SimpleSequenceDiagram.xml'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSequenceDiagramSerialization(self):

        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, TestSequenceDiagram.SEQUENCE_DIAGRAM_FILENAME)

        untangler:  UnTangler = UnTangler(xmlVersion=XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document = untangler.documents[DocumentTitle('SimpleSequence')]

        # we now have ogl objects to serialize

        oglToMiniDom: OglToMiniDomV10 = OglToMiniDomV10(projectVersion=untangler.projectInformation.version,
                                                        projectCodePath=untangler.projectInformation.codePath)
        oglDocument: OglDocument = OglDocument()
        oglDocument.toOglDocument(document=singleDocument)
        oglDocument.oglSDInstances = OglSDInstances(singleDocument.oglSDInstances)
        oglDocument.oglSDMessages  = OglSDMessages(singleDocument.oglSDMessages)

        oglToMiniDom.serialize(oglDocument=oglDocument)

        generatedFileName: str = ProjectTestBase.constructGeneratedName(TestSequenceDiagram.SEQUENCE_DIAGRAM_FILENAME)
        oglToMiniDom.writeXml(fqFileName=generatedFileName)

        status: int = self._runDiff(TestSequenceDiagram.SEQUENCE_DIAGRAM_FILENAME)

        self.assertEqual(0, status, 'Diff of sequence diagram serialization failed')

        ProjectTestBase.cleanupGenerated(TestSequenceDiagram.SEQUENCE_DIAGRAM_FILENAME)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestSequenceDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
