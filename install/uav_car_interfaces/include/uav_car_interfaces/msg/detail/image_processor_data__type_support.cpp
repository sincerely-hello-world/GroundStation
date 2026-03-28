// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "uav_car_interfaces/msg/detail/image_processor_data__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace uav_car_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ImageProcessorData_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) uav_car_interfaces::msg::ImageProcessorData(_init);
}

void ImageProcessorData_fini_function(void * message_memory)
{
  auto typed_message = static_cast<uav_car_interfaces::msg::ImageProcessorData *>(message_memory);
  typed_message->~ImageProcessorData();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ImageProcessorData_message_member_array[3] = {
  {
    "res_x",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces::msg::ImageProcessorData, res_x),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "res_y",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces::msg::ImageProcessorData, res_y),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "res_flag",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_car_interfaces::msg::ImageProcessorData, res_flag),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ImageProcessorData_message_members = {
  "uav_car_interfaces::msg",  // message namespace
  "ImageProcessorData",  // message name
  3,  // number of fields
  sizeof(uav_car_interfaces::msg::ImageProcessorData),
  ImageProcessorData_message_member_array,  // message members
  ImageProcessorData_init_function,  // function to initialize message memory (memory has to be allocated)
  ImageProcessorData_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ImageProcessorData_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ImageProcessorData_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace uav_car_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<uav_car_interfaces::msg::ImageProcessorData>()
{
  return &::uav_car_interfaces::msg::rosidl_typesupport_introspection_cpp::ImageProcessorData_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, uav_car_interfaces, msg, ImageProcessorData)() {
  return &::uav_car_interfaces::msg::rosidl_typesupport_introspection_cpp::ImageProcessorData_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
