
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from ogl.OglClass import OglClass

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutClassCommon import PyutClassCommon
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from oglio.Types import OglClasses
from oglio.toXmlV10.BaseOglToMiniDom import BaseOglToMiniDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglClassesToMiniDom(BaseOglToMiniDom):

    def __init__(self, xmlDocument: Document):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._xmlDocument: Document = xmlDocument

    def serialize(self, documentNode: Element, oglClasses: OglClasses) -> Element:

        for oglClass in oglClasses:
            classElement: Element = self._oglClassToXml(oglClass=oglClass, xmlDoc=self._xmlDocument)
            documentNode.appendChild(classElement)

        return documentNode

    def _oglClassToXml(self, oglClass: OglClass, xmlDoc: Document) -> Element:
        """
        Exports an OglClass to a minidom Element.

        Args:
            oglClass:   Graphic Class to save
            xmlDoc:     The document to append to

        Returns:
            The newly created `GraphicClass` element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_CLASS)

        root = self._appendOglBase(oglClass, root)

        # adding the data layer object
        root.appendChild(self._pyutClassToXml(cast(PyutClass, oglClass.pyutObject), xmlDoc))

        return root

    def _pyutClassToXml(self, pyutClass: PyutClass, xmlDoc: Document) -> Element:
        """
        Exporting a PyutClass to a miniDom Element.

        Args:
            pyutClass:  The pyut class to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        root = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_CLASS)

        classId: int = self._idFactory.getID(pyutClass)
        root.setAttribute(XmlConstants.ATTR_ID, str(classId))
        root.setAttribute(XmlConstants.ATTR_NAME, pyutClass.name)

        stereotype = pyutClass.stereotype
        if stereotype is not None:
            root.setAttribute(XmlConstants.ATTR_STEREOTYPE, stereotype.name)

        root.setAttribute(XmlConstants.ATTR_FILENAME, pyutClass.fileName)

        root = self._pyutClassCommonToXml(pyutClass, root)

        root.setAttribute(XmlConstants.ATTR_SHOW_METHODS, str(pyutClass.showMethods))
        root.setAttribute(XmlConstants.ATTR_SHOW_FIELDS, str(pyutClass.showFields))
        root.setAttribute(XmlConstants.ATTR_SHOW_STEREOTYPE, str(pyutClass.displayStereoType))
        root.setAttribute(XmlConstants.ATTR_DISPLAY_PARAMETERS, pyutClass.displayParameters.value)

        # methods
        for method in pyutClass.methods:
            root.appendChild(self._pyutMethodToXml(method, xmlDoc))
        # fields
        for field in pyutClass.fields:
            root.appendChild(self._pyutFieldToXml(field, xmlDoc))

        return root

    def _pyutMethodToXml(self, pyutMethod, xmlDoc) -> Element:
        """
        Exporting a PyutMethod to a miniDom Element

        Args:
            pyutMethod: Method to save
            xmlDoc:     xml document

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_METHOD)

        root.setAttribute(XmlConstants.ATTR_NAME, pyutMethod.name)

        visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
        visName:    str                = self.__safeVisibilityToName(visibility)

        if visibility is not None:
            root.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)

        for modifier in pyutMethod.modifiers:
            xmlModifier: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_MODIFIER)
            xmlModifier.setAttribute(XmlConstants.ATTR_NAME, modifier.name)
            root.appendChild(xmlModifier)

        if pyutMethod.returnType is not None:
            xmlReturnType: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_RETURN)
            xmlReturnType.setAttribute(XmlConstants.ATTR_TYPE, str(pyutMethod.returnType))
            root.appendChild(xmlReturnType)

        for param in pyutMethod.parameters:
            root.appendChild(self._pyutParamToXml(param, xmlDoc))

        codeRoot: Element = self._pyutSourceCodeToXml(pyutMethod.sourceCode, xmlDoc)
        root.appendChild(codeRoot)
        return root

    def _pyutFieldToXml(self, pyutField: PyutField, xmlDoc: Document) -> Element:
        """
        Export a PyutField to a miniDom Element
        Args:
            pyutField:  The PyutField to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_FIELD)

        root.appendChild(self._pyutParamToXml(pyutField, xmlDoc))
        visibility: PyutVisibilityEnum = pyutField.visibility
        visName:    str                = self.__safeVisibilityToName(visibility)
        root.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)

        return root

    def _pyutParamToXml(self, pyutParam: PyutParameter, xmlDoc: Document) -> Element:
        """
        Export a PyutParam to a miniDom Element

        Args:
            pyutParam:  Parameter to save
            xmlDoc:     XML Node

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_PARAM)

        root.setAttribute(XmlConstants.ATTR_NAME, pyutParam.name)
        root.setAttribute(XmlConstants.ATTR_TYPE, str(pyutParam.type))

        defaultValue = pyutParam.defaultValue
        if defaultValue is not None:
            root.setAttribute(XmlConstants.ATTR_DEFAULT_VALUE, defaultValue)

        return root

    def _pyutSourceCodeToXml(self, sourceCode: SourceCode, xmlDoc: Document) -> Element:

        codeRoot: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_SOURCE_CODE)
        for code in sourceCode:
            codeElement:  Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_CODE)
            textCodeNode: Element = xmlDoc.createTextNode(code)
            codeElement.appendChild(textCodeNode)
            codeRoot.appendChild(codeElement)

        return codeRoot

    def _pyutClassCommonToXml(self, classCommon: PyutClassCommon, root: Element) -> Element:

        root.setAttribute(XmlConstants.ATTR_DESCRIPTION, classCommon.description)
        # root.setAttribute(PyutXmlConstants.ATTR_FILENAME,    pyutInterface.getFilename())

        return root

    def __safeVisibilityToName(self, visibility: Union[str, PyutVisibilityEnum]) -> str:
        """
        Account for old pre V10 code
        Args:
            visibility:

        Returns:
            The visibility name
        """

        if isinstance(visibility, str):
            visStr: str = PyutVisibilityEnum.toEnum(visibility).name
        else:
            visStr = visibility.name

        return visStr
