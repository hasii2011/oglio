
from logging import Logger
from logging import getLogger
from typing import cast

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from ogl.OglUseCase import OglUseCase

from oglio.Types import OglUseCases
from oglio.toXmlV11.XmlConstants import XmlConstants

from oglio.toXmlV11.BaseOglToXml import BaseOglToXml
from oglio.toXmlV11.PyutToXml import PyutToXml


class OglUseCasesToXml(BaseOglToXml):
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglUseCases: OglUseCases) -> Element:

        for useCase in oglUseCases:
            oglUseCase:        OglUseCase = cast(OglUseCase, useCase)
            oglUseCaseElement: Element    = self._oglUseCaseToXml(documentTop=documentTop, oglUseCase=oglUseCase)
            self._pyutToXml.pyutUseCaseToXml(pyutUseCase=oglUseCase.pyutObject, oglUseCaseElement=oglUseCaseElement)

        return documentTop

    def _oglUseCaseToXml(self, documentTop: Element, oglUseCase: OglUseCase) -> Element:

        attributes = self._oglBaseAttributes(oglObject=oglUseCase)
        oglTextSubElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_USE_CASE, attrib=attributes)

        return oglTextSubElement

