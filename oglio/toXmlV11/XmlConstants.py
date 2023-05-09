
class XmlConstants:
    """
    A `no method` class that just hosts the strings that represent the Pyut XML strings
    """

    TOP_LEVEL_ELEMENT:           str = 'PyutProject'
    ELEMENT_OGL_CLASS:           str = 'OglClass'
    ELEMENT_GRAPHIC_LINK:        str = 'OglLink'
    ELEMENT_GRAPHIC_NOTE:        str = 'OglNote'

    ELEMENT_GRAPHIC_LOLLIPOP:    str = 'GraphicLollipop'
    ELEMENT_GRAPHIC_TEXT:        str = 'GraphicText'
    ELEMENT_GRAPHIC_ACTOR:       str = 'GraphicActor'
    ELEMENT_GRAPHIC_USE_CASE:    str = 'GraphicUseCase'
    ELEMENT_GRAPHIC_SD_INSTANCE: str = 'GraphicSDInstance'
    ELEMENT_GRAPHIC_SD_MESSAGE:  str = 'GraphicSDMessage'

    ELEMENT_DOCUMENT:             str = 'PyutDocument'
    ELEMENT_PYUT_CLASS:           str = 'PyutClass'
    ELEMENT_PYUT_METHOD:          str = 'PyutMethod'
    ELEMENT_MODEL_PYUT_PARAMETER: str = 'PyutParameter'
    ELEMENT_MODEL_PYUT_FIELD:     str = 'PyutField'
    ELEMENT_PYUT_LINK:            str = 'PyutLink'
    ELEMENT_PYUT_NOTE:            str = 'PyutNote'

    ELEMENT_MODEL_INTERFACE:      str = 'Interface'
    ELEMENT_IMPLEMENTOR:          str = 'Implementor'


    ELEMENT_MODEL_TEXT:        str = 'Text'
    ELEMENT_MODEL_ACTOR:       str = 'Actor'
    ELEMENT_MODEL_USE_CASE:    str = 'UseCase'
    ELEMENT_MODEL_MODIFIER:    str = 'Modifier'
    ELEMENT_MODEL_SOURCE_CODE: str = 'SourceCode'
    ELEMENT_MODEL_CODE:        str = 'Code'

    ELEMENT_MODEL_SD_INSTANCE:   str = 'SDInstance'
    ELEMENT_MODEL_SD_MESSAGE:    str = 'SDMessage'
    ELEMENT_MODEL_CONTROL_POINT: str = 'ControlPoint'

    ELEMENT_ASSOCIATION_CENTER_LABEL:      str = 'LabelCenter'
    ELEMENT_ASSOCIATION_SOURCE_LABEL:      str = 'LabelSource'
    ELEMENT_ASSOCIATION_DESTINATION_LABEL: str = 'LabelDestination'

    ATTR_VERSION: str = 'version'

    ATTR_ID: str = 'id'

    ATTR_WIDTH:  str = 'width'
    ATTR_HEIGHT: str = 'height'

    ATTR_X: str = 'x'
    ATTR_Y: str = 'y'

    ATTR_STEREOTYPE:  str = 'stereotype'
    ATTR_DESCRIPTION: str = 'description'
    ATTR_VISIBILITY:  str = 'visibility'

    ATTR_FILENAME: str = 'filename'
    ATTR_NAME:     str = 'name'
    ATTR_CONTENT:  str = 'content'
    ATTR_TYPE:     str = 'type'
    ATTR_TITLE:    str = 'title'

    ATTR_DEFAULT_VALUE:      str = 'defaultValue'
    ATTR_DISPLAY_STEREOTYPE: str = 'displayStereotype'
    ATTR_DISPLAY_METHODS:    str = 'displayMethods'
    ATTR_DISPLAY_FIELDS:     str = 'displayFields'
    ATTR_DISPLAY_PARAMETERS: str = 'displayParameters'

    ATTR_METHOD_RETURN_TYPE: str = 'returnType'

    ATTR_SPLINE:               str = 'spline'
    ATTR_LINK_SOURCE_ANCHOR_X: str = 'sourceAnchorX'
    ATTR_LINK_SOURCE_ANCHOR_Y: str = 'sourceAnchorY'

    ATTR_LINK_DESTINATION_ANCHOR_X: str = 'destinationAnchorX'
    ATTR_LINK_DESTINATION_ANCHOR_Y: str = 'destinationAnchorY'

    ATTR_BIDIRECTIONAL: str = 'bidirectional'

    ATTR_SOURCE_ID:      str = 'sourceId'
    ATTR_DESTINATION_ID: str = 'destinationId'

    ATTR_CARDINALITY_SOURCE:      str = 'cardinalitySource'
    ATTR_CARDINALITY_DESTINATION: str = 'cardinalityDestination'

    ATTR_INSTANCE_NAME:    str = 'instanceName'
    ATTR_LIFE_LINE_LENGTH: str = 'lifeLineLength'

    ATTR_MESSAGE:               str = 'message'
    ATTR_SOURCE_TIME_LINE:      str = 'srcTime'
    ATTR_DESTINATION_TIME_LINE: str = 'dstTime'

    ATTR_SD_MESSAGE_SOURCE_ID:      str = 'srcID'
    ATTR_SD_MESSAGE_DESTINATION_ID: str = 'dstID'

    V9_LINK_PREFIX: str = 'OGL_'

    ATTR_CODE_PATH: str = 'CodePath'

    ATTR_SCROLL_POSITION_X: str = 'scrollPositionX'
    ATTR_SCROLL_POSITION_Y: str = 'scrollPositionY'
    ATTR_PIXELS_PER_UNIT_X: str = 'pixelsPerUnitX'
    ATTR_PIXELS_PER_UNIT_Y: str = 'pixelsPerUnitY'

    ATTR_LOLLIPOP_ATTACHMENT_POINT: str = 'attachmentPoint'
    ATTR_IMPLEMENTING_CLASS_NAME:   str = 'implementingClassName'

    ATTR_TEXT_SIZE:     str = 'textSize'
    ATTR_IS_BOLD:       str = 'isBold'
    ATTR_IS_ITALICIZED: str = 'isItalicized'
    ATTR_FONT_FAMILY:   str = 'fontFamily'
