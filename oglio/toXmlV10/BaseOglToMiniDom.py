
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Union

from logging import Logger
from logging import getLogger
from xml.dom.minidom import Element

from ogl.OglObject import OglObject
from ogl.Singleton import Singleton             # TODO temp import this until get my common utilities module

from oglio.toXmlV10.XmlConstants import XmlConstants


class IDFactory(Singleton):
    """
    Type hinting results in self-documenting code. I really prefer and evangelize it.

    A user-defined class or class object is an instance of the object named `type`, which is itself a `class`. Classes
    are created from `type`, or in other words:

    >   A class is an instance of the class `type`.  In Python 3 there is no difference between `classes` and `types`
    """
    nextID: int = 1

    def init(self):
        """
        The singleton initialization method
        """
        self._classCache: Dict[type, int] = {}

    def getID(self, cls: Union[Any, type]):
        if cls in self._classCache:
            return self._classCache[cls]
        else:
            clsId = IDFactory.nextID
            self._classCache[cls] = clsId
            IDFactory.nextID += 1
            return clsId


class BaseOglToMiniDom:

    def __init__(self):

        self.baseLogger: Logger    = getLogger(__name__)
        self._idFactory: IDFactory = IDFactory()

    def _appendOglBase(self, oglObject: OglObject, root: Element) -> Element:
        """
        Saves the position and size of the OGL object in an ML node.

        Args:
            oglObject:  OGL Object
            root:      XML node to update

        Returns:
            The updated element
        """
        # Saving size
        w, h = oglObject.GetModel().GetSize()
        simpleW, simpleH = self._getSimpleDimensions(w, h)
        root.setAttribute(XmlConstants.ATTR_WIDTH, simpleW)
        root.setAttribute(XmlConstants.ATTR_HEIGHT, simpleH)

        # Saving position
        x, y = oglObject.GetModel().GetPosition()
        simpleX, simpleY = self._getSimpleCoordinates(x, y)
        root.setAttribute(XmlConstants.ATTR_X, simpleX)
        root.setAttribute(XmlConstants.ATTR_Y, simpleY)

        return root

    def _getSimpleDimensions(self, w: int, h: int) -> Tuple[str, str]:
        # reuse code but not name
        return self._getSimpleCoordinates(w, h)

    def _getSimpleCoordinates(self, x: int, y: int) -> Tuple[str, str]:
        """

        Args:
            x: coordinate
            y: coordinate

        Returns:
            Simple formatted string versions of the above

        """
        simpleX: str = str(int(x))      # some older files used float
        simpleY: str = str(int(y))      # some older files used float

        return simpleX, simpleY
