
from logging import Logger
from logging import getLogger
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutClassCommon import PyutClassCommon
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutParameter import PyutParameter

from oglio.toXmlV11.BaseXml import BaseXml
from oglio.toXmlV11.InternalTypes import ElementAttributes
from oglio.toXmlV11.XmlConstants import XmlConstants


class PyutToXml(BaseXml):
    """
    Serializes Pyut Models classes to DOM
    """
    # https://www.codetable.net/hex/a
    END_OF_LINE_MARKER: str ='&#xA;'

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def pyutClassToXml(self, pyutClass: PyutClass, graphicElement: Element) -> Element:
        """
        Exporting a PyutClass to a miniDom Element.

        Args:
            pyutClass:       The pyut class to save
            graphicElement:  The xml element to update

        Returns:
            A new updated element
        """

        commonAttributes = self._pyutClassCommonAttributes(pyutClass)
        attributes = {
            XmlConstants.ATTR_ID:                 str(pyutClass.id),
            XmlConstants.ATTR_NAME:               pyutClass.name,
            XmlConstants.ATTR_STEREOTYPE:         pyutClass.stereotype.value,
            XmlConstants.ATTR_DISPLAY_METHODS:    str(pyutClass.showMethods),
            XmlConstants.ATTR_DISPLAY_PARAMETERS: str(pyutClass.displayParameters),
            XmlConstants.ATTR_DISPLAY_FIELDS:     str(pyutClass.showFields),
            XmlConstants.ATTR_DISPLAY_STEREOTYPE: str(pyutClass.displayStereoType),
        }

        attributes = attributes | commonAttributes

        pyutClassElement: Element = SubElement(graphicElement, XmlConstants.ELEMENT_PYUT_CLASS, attrib=attributes)

        for method in pyutClass.methods:
            self._pyutMethodToXml(pyutMethod=method, pyutClassElement=pyutClassElement)

        for pyutField in pyutClass.fields:
            self._pyutFieldToXml(pyutField=pyutField, pyutClassElement=pyutClassElement)
        return pyutClassElement

    def pyutLinkToXml(self, pyutLink: PyutLink, oglLinkElement: Element) -> Element:
        """
        Exporting a PyutLink to an Element.

        Args:
            pyutLink:   Link to save
            oglLinkElement:     xml document

        Returns:
            A new minidom element
        """
        srcLinkId:  int = self._idFactory.getID(pyutLink.getSource())
        destLinkId: int = self._idFactory.getID(pyutLink.getDestination())

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_NAME:                    pyutLink.name,
            XmlConstants.ATTR_TYPE:                    pyutLink.linkType.name,
            XmlConstants.ATTR_CARDINALITY_SOURCE:      pyutLink.sourceCardinality,
            XmlConstants.ATTR_CARDINALITY_DESTINATION: pyutLink.destinationCardinality,
            XmlConstants.ATTR_BIDIRECTIONAL:           str(pyutLink.getBidir()),
            XmlConstants.ATTR_SOURCE_ID:               str(srcLinkId),
            XmlConstants.ATTR_DESTINATION_ID:          str(destLinkId),
        })
        pyutLinkElement: Element = SubElement(oglLinkElement, XmlConstants.ELEMENT_PYUT_LINK, attrib=attributes)
        # root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_LINK)
        #
        # root.setAttribute(XmlConstants.ATTR_NAME, pyutLink.name)
        # root.setAttribute(XmlConstants.ATTR_TYPE, pyutLink.linkType.name)
        # root.setAttribute(XmlConstants.ATTR_CARDINALITY_SOURCE, pyutLink.sourceCardinality)
        # root.setAttribute(XmlConstants.ATTR_CARDINALITY_DESTINATION, pyutLink.destinationCardinality)
        # root.setAttribute(XmlConstants.ATTR_BIDIRECTIONAL, str(pyutLink.getBidir()))
        #
        # srcLinkId:  int = self._idFactory.getID(pyutLink.getSource())
        # destLinkId: int = self._idFactory.getID(pyutLink.getDestination())
        #
        # root.setAttribute(XmlConstants.ATTR_SOURCE_ID, str(srcLinkId))
        # root.setAttribute(XmlConstants.ATTR_DESTINATION_ID, str(destLinkId))
        #
        # return root
        return pyutLinkElement

    def _pyutMethodToXml(self, pyutMethod: PyutMethod, pyutClassElement: Element) -> Element:
        """
        Exporting a PyutMethod to an Element

        Args:
            pyutMethod:        Method to serialize
            pyutClassElement:  xml document

        Returns:
            The new updated element
        """
        attributes = {
            XmlConstants.ATTR_NAME:               pyutMethod.name,
            XmlConstants.ATTR_VISIBILITY:         pyutMethod.visibility.name,
            XmlConstants.ATTR_METHOD_RETURN_TYPE: pyutMethod.returnType.value,
        }
        pyutMethodElement: Element = SubElement(pyutClassElement, XmlConstants.ELEMENT_PYUT_METHOD, attrib=attributes)
        for modifier in pyutMethod.modifiers:
            attributes = {
                XmlConstants.ATTR_NAME: modifier.name,
            }
            SubElement(pyutMethodElement, XmlConstants.ELEMENT_MODEL_MODIFIER, attrib=attributes)
        self._pyutSourceCodeToXml(pyutMethod.sourceCode, pyutMethodElement)

        for pyutParameter in pyutMethod.parameters:
            self._pyutParameterToXml(pyutParameter, pyutMethodElement)
        # pyutMethodElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_METHOD)
        #
        # pyutMethodElement.setAttribute(XmlConstants.ATTR_NAME, pyutMethod.name)
        #
        # visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
        # visName:    str                = self.__safeVisibilityToName(visibility)
        #
        # if visibility is not None:
        #     pyutMethodElement.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)
        #
        # for modifier in pyutMethod.modifiers:
        #     xmlModifier: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_MODIFIER)
        #     xmlModifier.setAttribute(XmlConstants.ATTR_NAME, modifier.name)
        #     pyutMethodElement.appendChild(xmlModifier)
        #
        # if pyutMethod.returnType is not None:
        #     xmlReturnType: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_RETURN)
        #     xmlReturnType.setAttribute(XmlConstants.ATTR_TYPE, str(pyutMethod.returnType))
        #     pyutMethodElement.appendChild(xmlReturnType)
        #
        # for param in pyutMethod.parameters:
        #     pyutMethodElement.appendChild(self._pyutParamToDom(param, xmlDoc))
        #
        # codeRoot: Element = self._pyutSourceCodeToDom(pyutMethod.sourceCode, xmlDoc)
        # pyutMethodElement.appendChild(codeRoot)
        # return pyutMethodElement
        return pyutMethodElement

    def _pyutClassCommonAttributes(self, classCommon: PyutClassCommon):

        attributes = {
            XmlConstants.ATTR_DESCRIPTION: classCommon.description
        }
        return attributes

    def _pyutSourceCodeToXml(self, sourceCode: SourceCode, pyutMethodElement: Element):

        codeRoot: Element = SubElement(pyutMethodElement, XmlConstants.ELEMENT_MODEL_SOURCE_CODE)

        for code in sourceCode:
            codeElement: Element = SubElement(codeRoot, XmlConstants.ELEMENT_MODEL_CODE)
            codeElement.text = code

        return codeRoot

    def _pyutParameterToXml(self, pyutParameter: PyutParameter, pyutMethodElement: Element) -> Element:

        attributes = {
            XmlConstants.ATTR_NAME:          pyutParameter.name,
            XmlConstants.ATTR_TYPE:          pyutParameter.type.value,
            XmlConstants.ATTR_DEFAULT_VALUE: pyutParameter.defaultValue,
        }
        pyutParameterElement: Element = SubElement(pyutMethodElement, XmlConstants.ELEMENT_MODEL_PYUT_PARAMETER, attrib=attributes)

        return pyutParameterElement

    def _pyutFieldToXml(self, pyutField: PyutField, pyutClassElement: Element) -> Element:
        """
        Serialize a PyutField to an Element

        Args:
            pyutField:         The PyutField to serialize
            pyutClassElement: The Pyut Class element to update

        Returns:
            The new updated element
        """
        attributes = {
            XmlConstants.ATTR_NAME:          pyutField.name,
            XmlConstants.ATTR_VISIBILITY:    pyutField.visibility.name,
            XmlConstants.ATTR_TYPE:          pyutField.type.value,
            XmlConstants.ATTR_DEFAULT_VALUE: pyutField.defaultValue,
        }
        pyutFieldElement: Element = SubElement(pyutClassElement, XmlConstants.ELEMENT_MODEL_PYUT_FIELD, attrib=attributes)

        return pyutFieldElement