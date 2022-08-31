
import json

import logging
import logging.config

from os import system as osSystem
from os import sep as osSep

from pkg_resources import resource_filename

from miniogl.DiagramFrame import DiagramFrame
from pyutmodel.PyutObject import PyutObject

from wx import App
from wx import Frame
from wx import ID_ANY

from unittest import TestCase

from oglio.toXmlV10.BaseToDom import IDFactory

JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'


class BogusApp(App):
    def OnInit(self) -> bool:
        return True


class TestBase(TestCase):

    RESOURCES_PACKAGE_NAME:                      str = 'tests.resources'
    RESOURCES_TEST_CLASSES_PACKAGE_NAME:         str = f'{RESOURCES_PACKAGE_NAME}.testclasses'
    RESOURCES_TEST_DATA_PACKAGE_NAME:            str = f'{RESOURCES_PACKAGE_NAME}.testdata'

    EXTERNAL_DIFF:         str = '/usr/bin/diff -w '
    EXTERNAL_CLEAN_UP_TMP: str = 'rm '

    def setUp(self):
        """
        Test classes that need to instantiate a wxPython App should super().setUp()
        """
        self._app:   BogusApp = BogusApp()
        baseFrame:   Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = DiagramFrame(baseFrame)
        umlFrame.Show(True)
        PyutObject.nextID = 0   # reset to match sequence diagram
        IDFactory.nextID  = 1

    def tearDown(self):
        self._app.OnExit()

    """
    A base unit test class to initialize some logging stuff we need
    """
    @classmethod
    def setUpLogging(cls):
        """"""
        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:

        fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName

    def _runDiff(self, fileName: str) -> int:

        baseFileName:      str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, fileName)
        generatedFileName: str = self._constructGeneratedName(fileName=fileName)

        status: int = osSystem(f'{TestBase.EXTERNAL_DIFF} {baseFileName} {generatedFileName}')

        return status

    def _cleanupGenerated(self, fileName: str):

        generatedFileName: str = self._constructGeneratedName(fileName=fileName)

        osSystem(f'{TestBase.EXTERNAL_CLEAN_UP_TMP} {generatedFileName}')

    def _constructGeneratedName(self, fileName: str) -> str:

        generatedFileName: str = f'{osSep}tmp{osSep}{fileName}'
        return generatedFileName
