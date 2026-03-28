// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "uav_car_interfaces/msg/detail/image_processor_data__rosidl_typesupport_introspection_c.h"
#include "uav_car_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "uav_car_interfaces/msg/detail/image_processor_data__functions.h"
#include "uav_car_interfaces/msg/detail/image_processor_data__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  uav_car_interfaces__msg__ImageProcessorData__init(message_memory);
}

void ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_fini_function(void * message_memory)
{
  uav_car_interfaces__msg__ImageProcessorData__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_message_member_array[3] = {
  {
    "res_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces__msg__ImageProcessorData, res_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "res_y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces__msg__ImageProcessorData, res_y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "res_flag",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces__msg__ImageProcessorData, res_flag),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_message_members = {
  "uav_car_interfaces__msg",  // message namespace
  "ImageProcessorData",  // message name
  3,  // number of fields
  sizeof(uav_car_interfaces__msg__ImageProcessorData),
  ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_message_member_array,  // message members
  ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_init_function,  // function to initialize message memory (memory has to be allocated)
  ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_message_type_support_handle = {
  0,
  &ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_uav_car_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, uav_car_interfaces, msg, ImageProcessorData)() {
  if (!ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_message_type_support_handle.typesupport_identifier) {
    ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ImageProcessorData__rosidl_typesupport_introspection_c__ImageProcessorData_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
