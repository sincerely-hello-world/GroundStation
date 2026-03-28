// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice
#include "uav_car_interfaces/msg/detail/image_processor_data__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "uav_car_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "uav_car_interfaces/msg/detail/image_processor_data__struct.h"
#include "uav_car_interfaces/msg/detail/image_processor_data__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _ImageProcessorData__ros_msg_type = uav_car_interfaces__msg__ImageProcessorData;

static bool _ImageProcessorData__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ImageProcessorData__ros_msg_type * ros_message = static_cast<const _ImageProcessorData__ros_msg_type *>(untyped_ros_message);
  // Field name: res_x
  {
    cdr << ros_message->res_x;
  }

  // Field name: res_y
  {
    cdr << ros_message->res_y;
  }

  // Field name: res_flag
  {
    cdr << ros_message->res_flag;
  }

  return true;
}

static bool _ImageProcessorData__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ImageProcessorData__ros_msg_type * ros_message = static_cast<_ImageProcessorData__ros_msg_type *>(untyped_ros_message);
  // Field name: res_x
  {
    cdr >> ros_message->res_x;
  }

  // Field name: res_y
  {
    cdr >> ros_message->res_y;
  }

  // Field name: res_flag
  {
    cdr >> ros_message->res_flag;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_uav_car_interfaces
size_t get_serialized_size_uav_car_interfaces__msg__ImageProcessorData(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ImageProcessorData__ros_msg_type * ros_message = static_cast<const _ImageProcessorData__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name res_x
  {
    size_t item_size = sizeof(ros_message->res_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name res_y
  {
    size_t item_size = sizeof(ros_message->res_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name res_flag
  {
    size_t item_size = sizeof(ros_message->res_flag);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _ImageProcessorData__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_uav_car_interfaces__msg__ImageProcessorData(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_uav_car_interfaces
size_t max_serialized_size_uav_car_interfaces__msg__ImageProcessorData(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: res_x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: res_y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: res_flag
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static size_t _ImageProcessorData__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_uav_car_interfaces__msg__ImageProcessorData(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_ImageProcessorData = {
  "uav_car_interfaces::msg",
  "ImageProcessorData",
  _ImageProcessorData__cdr_serialize,
  _ImageProcessorData__cdr_deserialize,
  _ImageProcessorData__get_serialized_size,
  _ImageProcessorData__max_serialized_size
};

static rosidl_message_type_support_t _ImageProcessorData__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ImageProcessorData,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, msg, ImageProcessorData)() {
  return &_ImageProcessorData__type_support;
}

#if defined(__cplusplus)
}
#endif
