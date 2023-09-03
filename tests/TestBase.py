
from os import system as osSystem
from os import sep as osSep
from os import environ as osEnviron

from hasiihelper.UnitTestBase import UnitTestBase
from hasiicommon.ui.UnitTestBaseW import UnitTestBaseW

from pyutmodel.PyutObject import PyutObject

from oglio.toXmlV10.BaseToDom import IDFactory


class TestBase(UnitTestBaseW):

    RESOURCES_TEST_CLASSES_PACKAGE_NAME:         str = f'{UnitTestBase.RESOURCES_PACKAGE_NAME}.testclasses'
    RESOURCES_TEST_DATA_PACKAGE_NAME:            str = f'{UnitTestBase.RESOURCES_PACKAGE_NAME}.testdata'

    EXTERNAL_DIFF:         str = '/usr/bin/diff -w '
    EXTERNAL_CLEAN_UP_TMP: str = 'rm -rf'

    keep:      bool   = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if 'KEEP' in osEnviron:
            keep: str = osEnviron["KEEP"]
            if keep.lower().strip() == 'true':
                cls.keep = True
            else:
                cls.keep = False
        else:
            cls.clsLogger.debug(f'No need to keep data files')
            cls.keep = False

    def setUp(self):
        super().setUp()
        PyutObject.nextId = 0   # reset to match sequence diagram
        IDFactory.nextID  = 1

    def tearDown(self):
        super().tearDown()

    def _runDiff(self, fileName: str) -> int:

        baseFileName:      str = TestBase.getFullyQualifiedResourceFileName(package=TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, fileName=fileName)
        generatedFileName: str = TestBase.constructGeneratedName(fileName=fileName)

        status: int = osSystem(f'{TestBase.EXTERNAL_DIFF} {baseFileName} {generatedFileName}')

        return status

    @classmethod
    def cleanupGenerated(cls, fileName: str):

        generatedFileName: str = cls.constructGeneratedName(fileName=fileName)

        if TestBase.keep is False:
            osSystem(f'{TestBase.EXTERNAL_CLEAN_UP_TMP} {generatedFileName}')

    @classmethod
    def constructGeneratedName(cls, fileName: str) -> str:

        generatedFileName: str = f'{osSep}tmp{osSep}{fileName}'
        return generatedFileName
