# generated from rosidl_generator_py/resource/_idl.py.em
# with input from uav_car_interfaces:msg/ImageProcessorData.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ImageProcessorData(type):
    """Metaclass of message 'ImageProcessorData'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('uav_car_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'uav_car_interfaces.msg.ImageProcessorData')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__image_processor_data
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__image_processor_data
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__image_processor_data
            cls._TYPE_SUPPORT = module.type_support_msg__msg__image_processor_data
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__image_processor_data

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ImageProcessorData(metaclass=Metaclass_ImageProcessorData):
    """Message class 'ImageProcessorData'."""

    __slots__ = [
        '_res_x',
        '_res_y',
        '_res_flag',
    ]

    _fields_and_field_types = {
        'res_x': 'int8',
        'res_y': 'int8',
        'res_flag': 'int8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.res_x = kwargs.get('res_x', int())
        self.res_y = kwargs.get('res_y', int())
        self.res_flag = kwargs.get('res_flag', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.res_x != other.res_x:
            return False
        if self.res_y != other.res_y:
            return False
        if self.res_flag != other.res_flag:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @property
    def res_x(self):
        """Message field 'res_x'."""
        return self._res_x

    @res_x.setter
    def res_x(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'res_x' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'res_x' field must be an integer in [-128, 127]"
        self._res_x = value

    @property
    def res_y(self):
        """Message field 'res_y'."""
        return self._res_y

    @res_y.setter
    def res_y(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'res_y' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'res_y' field must be an integer in [-128, 127]"
        self._res_y = value

    @property
    def res_flag(self):
        """Message field 'res_flag'."""
        return self._res_flag

    @res_flag.setter
    def res_flag(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'res_flag' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'res_flag' field must be an integer in [-128, 127]"
        self._res_flag = value
