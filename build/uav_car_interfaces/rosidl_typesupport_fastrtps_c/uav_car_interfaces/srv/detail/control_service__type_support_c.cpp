// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from uav_car_interfaces:srv/ControlService.idl
// generated code does not contain a copyright notice
#include "uav_car_interfaces/srv/detail/control_service__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "uav_car_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "uav_car_interfaces/srv/detail/control_service__struct.h"
#include "uav_car_interfaces/srv/detail/control_service__functions.h"
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

#include "rosidl_runtime_c/string.h"  // req
#include "rosidl_runtime_c/string_functions.h"  // req

// forward declare type support functions


using _ControlService_Request__ros_msg_type = uav_car_interfaces__srv__ControlService_Request;

static bool _ControlService_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ControlService_Request__ros_msg_type * ros_message = static_cast<const _ControlService_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: req
  {
    const rosidl_runtime_c__String * str = &ros_message->req;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _ControlService_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ControlService_Request__ros_msg_type * ros_message = static_cast<_ControlService_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: req
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->req.data) {
      rosidl_runtime_c__String__init(&ros_message->req);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->req,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'req'\n");
      return false;
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_uav_car_interfaces
size_t get_serialized_size_uav_car_interfaces__srv__ControlService_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ControlService_Request__ros_msg_type * ros_message = static_cast<const _ControlService_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name req
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->req.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _ControlService_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_uav_car_interfaces__srv__ControlService_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_uav_car_interfaces
size_t max_serialized_size_uav_car_interfaces__srv__ControlService_Request(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: req
  {
    size_t array_size = 1;

    full_bounded = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  return current_alignment - initial_alignment;
}

static size_t _ControlService_Request__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_uav_car_interfaces__srv__ControlService_Request(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_ControlService_Request = {
  "uav_car_interfaces::srv",
  "ControlService_Request",
  _ControlService_Request__cdr_serialize,
  _ControlService_Request__cdr_deserialize,
  _ControlService_Request__get_serialized_size,
  _ControlService_Request__max_serialized_size
};

static rosidl_message_type_support_t _ControlService_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ControlService_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, srv, ControlService_Request)() {
  return &_ControlService_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "uav_car_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "uav_car_interfaces/srv/detail/control_service__struct.h"
// already included above
// #include "uav_car_interfaces/srv/detail/control_service__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

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

// already included above
// #include "rosidl_runtime_c/string.h"  // echo
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // echo

// forward declare type support functions


using _ControlService_Response__ros_msg_type = uav_car_interfaces__srv__ControlService_Response;

static bool _ControlService_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ControlService_Response__ros_msg_type * ros_message = static_cast<const _ControlService_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: echo
  {
    const rosidl_runtime_c__String * str = &ros_message->echo;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _ControlService_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ControlService_Response__ros_msg_type * ros_message = static_cast<_ControlService_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: echo
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->echo.data) {
      rosidl_runtime_c__String__init(&ros_message->echo);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->echo,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'echo'\n");
      return false;
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_uav_car_interfaces
size_t get_serialized_size_uav_car_interfaces__srv__ControlService_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ControlService_Response__ros_msg_type * ros_message = static_cast<const _ControlService_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name echo
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->echo.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _ControlService_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_uav_car_interfaces__srv__ControlService_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_uav_car_interfaces
size_t max_serialized_size_uav_car_interfaces__srv__ControlService_Response(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: echo
  {
    size_t array_size = 1;

    full_bounded = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  return current_alignment - initial_alignment;
}

static size_t _ControlService_Response__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_uav_car_interfaces__srv__ControlService_Response(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_ControlService_Response = {
  "uav_car_interfaces::srv",
  "ControlService_Response",
  _ControlService_Response__cdr_serialize,
  _ControlService_Response__cdr_deserialize,
  _ControlService_Response__get_serialized_size,
  _ControlService_Response__max_serialized_size
};

static rosidl_message_type_support_t _ControlService_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ControlService_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, srv, ControlService_Response)() {
  return &_ControlService_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "uav_car_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "uav_car_interfaces/srv/control_service.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t ControlService__callbacks = {
  "uav_car_interfaces::srv",
  "ControlService",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, srv, ControlService_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, srv, ControlService_Response)(),
};

static rosidl_service_type_support_t ControlService__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &ControlService__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, srv, ControlService)() {
  return &ControlService__handle;
}

#if defined(__cplusplus)
}
#endif
