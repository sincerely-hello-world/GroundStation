// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice
#include "uav_car_interfaces/msg/detail/image_processor_data__rosidl_typesupport_fastrtps_cpp.hpp"
#include "uav_car_interfaces/msg/detail/image_processor_data__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace uav_car_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_uav_car_interfaces
cdr_serialize(
  const uav_car_interfaces::msg::ImageProcessorData & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: res_x
  cdr << ros_message.res_x;
  // Member: res_y
  cdr << ros_message.res_y;
  // Member: res_flag
  cdr << ros_message.res_flag;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_uav_car_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  uav_car_interfaces::msg::ImageProcessorData & ros_message)
{
  // Member: res_x
  cdr >> ros_message.res_x;

  // Member: res_y
  cdr >> ros_message.res_y;

  // Member: res_flag
  cdr >> ros_message.res_flag;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_uav_car_interfaces
get_serialized_size(
  const uav_car_interfaces::msg::ImageProcessorData & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: res_x
  {
    size_t item_size = sizeof(ros_message.res_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: res_y
  {
    size_t item_size = sizeof(ros_message.res_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: res_flag
  {
    size_t item_size = sizeof(ros_message.res_flag);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_uav_car_interfaces
max_serialized_size_ImageProcessorData(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: res_x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: res_y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: res_flag
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static bool _ImageProcessorData__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const uav_car_interfaces::msg::ImageProcessorData *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _ImageProcessorData__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<uav_car_interfaces::msg::ImageProcessorData *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _ImageProcessorData__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const uav_car_interfaces::msg::ImageProcessorData *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _ImageProcessorData__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_ImageProcessorData(full_bounded, 0);
}

static message_type_support_callbacks_t _ImageProcessorData__callbacks = {
  "uav_car_interfaces::msg",
  "ImageProcessorData",
  _ImageProcessorData__cdr_serialize,
  _ImageProcessorData__cdr_deserialize,
  _ImageProcessorData__get_serialized_size,
  _ImageProcessorData__max_serialized_size
};

static rosidl_message_type_support_t _ImageProcessorData__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_ImageProcessorData__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace uav_car_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_uav_car_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<uav_car_interfaces::msg::ImageProcessorData>()
{
  return &uav_car_interfaces::msg::typesupport_fastrtps_cpp::_ImageProcessorData__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, uav_car_interfaces, msg, ImageProcessorData)() {
  return &uav_car_interfaces::msg::typesupport_fastrtps_cpp::_ImageProcessorData__handle;
}

#ifdef __cplusplus
}
#endif
