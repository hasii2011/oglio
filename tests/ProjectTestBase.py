
from os import system as osSystem
from os import sep as osSep
from os import environ as osEnviron

from codeallybasic.UnitTestBase import UnitTestBase
from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from pyutmodelv2.PyutObject import PyutObject
from pyutmodelv2.PyutObject import infiniteSequence


class ProjectTestBase(UnitTestBaseW):

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
        PyutObject.idGenerator = infiniteSequence()
        next(PyutObject.idGenerator)

    def tearDown(self):
        super().tearDown()

    def _runDiff(self, fileName: str) -> int:

        baseFileName:      str = ProjectTestBase.getFullyQualifiedResourceFileName(package=ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, fileName=fileName)
        generatedFileName: str = ProjectTestBase.constructGeneratedName(fileName=fileName)

        status: int = osSystem(f'{ProjectTestBase.EXTERNAL_DIFF} {baseFileName} {generatedFileName}')

        return status

    @classmethod
    def cleanupGenerated(cls, fileName: str):

        generatedFileName: str = cls.constructGeneratedName(fileName=fileName)

        if ProjectTestBase.keep is False:
            osSystem(f'{ProjectTestBase.EXTERNAL_CLEAN_UP_TMP} {generatedFileName}')

    @classmethod
    def constructGeneratedName(cls, fileName: str) -> str:

        generatedFileName: str = f'{osSep}tmp{osSep}{fileName}'
        return generatedFileName
