// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from uav_car_interfaces:msg/T265Data.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "uav_car_interfaces/msg/detail/t265_data__rosidl_typesupport_introspection_c.h"
#include "uav_car_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "uav_car_interfaces/msg/detail/t265_data__functions.h"
#include "uav_car_interfaces/msg/detail/t265_data__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void T265Data__rosidl_typesupport_introspection_c__T265Data_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  uav_car_interfaces__msg__T265Data__init(message_memory);
}

void T265Data__rosidl_typesupport_introspection_c__T265Data_fini_function(void * message_memory)
{
  uav_car_interfaces__msg__T265Data__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember T265Data__rosidl_typesupport_introspection_c__T265Data_message_member_array[4] = {
  {
    "pos_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces__msg__T265Data, pos_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pos_y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces__msg__T265Data, pos_y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pos_z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces__msg__T265Data, pos_z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "confidence",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces__msg__T265Data, confidence),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers T265Data__rosidl_typesupport_introspection_c__T265Data_message_members = {
  "uav_car_interfaces__msg",  // message namespace
  "T265Data",  // message name
  4,  // number of fields
  sizeof(uav_car_interfaces__msg__T265Data),
  T265Data__rosidl_typesupport_introspection_c__T265Data_message_member_array,  // message members
  T265Data__rosidl_typesupport_introspection_c__T265Data_init_function,  // function to initialize message memory (memory has to be allocated)
  T265Data__rosidl_typesupport_introspection_c__T265Data_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t T265Data__rosidl_typesupport_introspection_c__T265Data_message_type_support_handle = {
  0,
  &T265Data__rosidl_typesupport_introspection_c__T265Data_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_uav_car_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, uav_car_interfaces, msg, T265Data)() {
  if (!T265Data__rosidl_typesupport_introspection_c__T265Data_message_type_support_handle.typesupport_identifier) {
    T265Data__rosidl_typesupport_introspection_c__T265Data_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &T265Data__rosidl_typesupport_introspection_c__T265Data_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
