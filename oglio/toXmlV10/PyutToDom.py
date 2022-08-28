
from typing import Union

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from pyutmodel.ModelTypes import ClassName
from pyutmodel.PyutActor import PyutActor
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutUseCase import PyutUseCase
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from oglio.toXmlV10.BasePyutToDom import BasePyutToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class PyutToDom(BasePyutToDom):

    def __init__(self):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def pyutClassToXml(self, pyutClass: PyutClass, xmlDoc: Document) -> Element:
        """
        Exporting a PyutClass to a miniDom Element.

        Args:
            pyutClass:  The pyut class to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        pyutClassElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_CLASS)

        classId: int = self._idFactory.getID(pyutClass)
        pyutClassElement.setAttribute(XmlConstants.ATTR_ID, str(classId))
        pyutClassElement.setAttribute(XmlConstants.ATTR_NAME, pyutClass.name)

        stereotype = pyutClass.stereotype
        if stereotype is not None:
            pyutClassElement.setAttribute(XmlConstants.ATTR_STEREOTYPE, stereotype.name)

        pyutClassElement.setAttribute(XmlConstants.ATTR_FILENAME, pyutClass.fileName)

        pyutClassElement = self._pyutClassCommonToXml(pyutClass, pyutClassElement)

        pyutClassElement.setAttribute(XmlConstants.ATTR_SHOW_METHODS, str(pyutClass.showMethods))
        pyutClassElement.setAttribute(XmlConstants.ATTR_SHOW_FIELDS, str(pyutClass.showFields))
        pyutClassElement.setAttribute(XmlConstants.ATTR_SHOW_STEREOTYPE, str(pyutClass.displayStereoType))
        pyutClassElement.setAttribute(XmlConstants.ATTR_DISPLAY_PARAMETERS, pyutClass.displayParameters.value)

        # methods
        for method in pyutClass.methods:
            pyutClassElement.appendChild(self._pyutMethodToXml(method, xmlDoc))
        # fields
        for field in pyutClass.fields:
            pyutClassElement.appendChild(self._pyutFieldToXml(field, xmlDoc))

        return pyutClassElement

    def pyutInterfaceToXml(self, pyutInterface: PyutInterface, xmlDoc: Document) -> Element:

        pyutInterfaceElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_INTERFACE)

        classId: int = self._idFactory.getID(pyutInterface)
        pyutInterfaceElement.setAttribute(XmlConstants.ATTR_ID, str(classId))
        pyutInterfaceElement.setAttribute(XmlConstants.ATTR_NAME, pyutInterface.name)

        pyutInterfaceElement = self._pyutClassCommonToXml(pyutInterface, pyutInterfaceElement)

        for method in pyutInterface.methods:
            pyutInterfaceElement.appendChild(self._pyutMethodToXml(method, xmlDoc))

        for className in pyutInterface.implementors:
            self.logger.debug(f'implementing className: {className}')
            pyutInterfaceElement.appendChild(self._pyutImplementorToXml(className, xmlDoc))

        return pyutInterfaceElement

    def pyutLinkToXml(self, pyutLink: PyutLink, xmlDoc: Document) -> Element:
        """
        Exporting a PyutLink to a miniDom Element.

        Args:
            pyutLink:   Link to save
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_LINK)

        root.setAttribute(XmlConstants.ATTR_NAME, pyutLink.name)
        root.setAttribute(XmlConstants.ATTR_TYPE, pyutLink.linkType.name)
        root.setAttribute(XmlConstants.ATTR_CARDINALITY_SOURCE, pyutLink.sourceCardinality)
        root.setAttribute(XmlConstants.ATTR_CARDINALITY_DESTINATION, pyutLink.destinationCardinality)
        root.setAttribute(XmlConstants.ATTR_BIDIRECTIONAL, str(pyutLink.getBidir()))

        srcLinkId:  int = self._idFactory.getID(pyutLink.getSource())
        destLinkId: int = self._idFactory.getID(pyutLink.getDestination())

        root.setAttribute(XmlConstants.ATTR_SOURCE_ID, str(srcLinkId))
        root.setAttribute(XmlConstants.ATTR_DESTINATION_ID, str(destLinkId))

        return root

    def pyutUseCaseToXml(self, pyutUseCase: PyutUseCase, xmlDoc: Document) -> Element:
        """
        Export a PyutUseCase to a minidom Element.

        Args:
            pyutUseCase:    Use case to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        pyutUseCaseElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_USE_CASE)

        useCaseId = self._idFactory.getID(pyutUseCase)
        pyutUseCaseElement.setAttribute(XmlConstants.ATTR_ID, str(useCaseId))
        pyutUseCaseElement.setAttribute(XmlConstants.ATTR_NAME, pyutUseCase.name)
        pyutUseCaseElement.setAttribute(XmlConstants.ATTR_FILENAME, pyutUseCase.fileName)

        return pyutUseCaseElement

    def pyutActorToXml(self, pyutActor: PyutActor, xmlDoc: Document) -> Element:
        """
        Export an PyutActor to a minidom Element.
        Args:
            pyutActor:  Actor to convert
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        pyutActorElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_ACTOR)

        actorId = self._idFactory.getID(pyutActor)
        pyutActorElement.setAttribute(XmlConstants.ATTR_ID, str(actorId))
        pyutActorElement.setAttribute(XmlConstants.ATTR_NAME, pyutActor.name)
        pyutActorElement.setAttribute(XmlConstants.ATTR_FILENAME, pyutActor.fileName)

        return pyutActorElement

    def _pyutMethodToXml(self, pyutMethod, xmlDoc) -> Element:
        """
        Exporting a PyutMethod to a miniDom Element

        Args:
            pyutMethod: Method to save
            xmlDoc:     xml document

        Returns:
            The new updated element
        """
        pyutMethodElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_METHOD)

        pyutMethodElement.setAttribute(XmlConstants.ATTR_NAME, pyutMethod.name)

        visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
        visName:    str                = self.__safeVisibilityToName(visibility)

        if visibility is not None:
            pyutMethodElement.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)

        for modifier in pyutMethod.modifiers:
            xmlModifier: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_MODIFIER)
            xmlModifier.setAttribute(XmlConstants.ATTR_NAME, modifier.name)
            pyutMethodElement.appendChild(xmlModifier)

        if pyutMethod.returnType is not None:
            xmlReturnType: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_RETURN)
            xmlReturnType.setAttribute(XmlConstants.ATTR_TYPE, str(pyutMethod.returnType))
            pyutMethodElement.appendChild(xmlReturnType)

        for param in pyutMethod.parameters:
            pyutMethodElement.appendChild(self._pyutParamToXml(param, xmlDoc))

        codeRoot: Element = self._pyutSourceCodeToXml(pyutMethod.sourceCode, xmlDoc)
        pyutMethodElement.appendChild(codeRoot)
        return pyutMethodElement

    def _pyutFieldToXml(self, pyutField: PyutField, xmlDoc: Document) -> Element:
        """
        Export a PyutField to a miniDom Element
        Args:
            pyutField:  The PyutField to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        pyutFieldElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_FIELD)

        pyutFieldElement.appendChild(self._pyutParamToXml(pyutField, xmlDoc))
        visibility: PyutVisibilityEnum = pyutField.visibility
        visName:    str                = self.__safeVisibilityToName(visibility)
        pyutFieldElement.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)

        return pyutFieldElement

    def _pyutParamToXml(self, pyutParam: PyutParameter, xmlDoc: Document) -> Element:
        """
        Export a PyutParam to a miniDom Element

        Args:
            pyutParam:  Parameter to save
            xmlDoc:     XML Node

        Returns:
            The new updated element
        """
        pyutParameterElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_PARAM)

        pyutParameterElement.setAttribute(XmlConstants.ATTR_NAME, pyutParam.name)
        pyutParameterElement.setAttribute(XmlConstants.ATTR_TYPE, str(pyutParam.type))

        defaultValue = pyutParam.defaultValue
        if defaultValue is not None:
            pyutParameterElement.setAttribute(XmlConstants.ATTR_DEFAULT_VALUE, defaultValue)

        return pyutParameterElement

    def _pyutSourceCodeToXml(self, sourceCode: SourceCode, xmlDoc: Document) -> Element:

        codeRoot: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_SOURCE_CODE)
        for code in sourceCode:
            codeElement:  Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_CODE)
            textCodeNode: Element = xmlDoc.createTextNode(code)
            codeElement.appendChild(textCodeNode)
            codeRoot.appendChild(codeElement)

        return codeRoot

    def _pyutImplementorToXml(self, className: ClassName, xmlDoc: Document) -> Element:

        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_IMPLEMENTOR)

        root.setAttribute(XmlConstants.ATTR_IMPLEMENTING_CLASS_NAME, className)

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
