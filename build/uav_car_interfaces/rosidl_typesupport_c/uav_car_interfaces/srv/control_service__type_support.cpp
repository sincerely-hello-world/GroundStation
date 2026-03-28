// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from uav_car_interfaces:srv/ControlService.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "uav_car_interfaces/msg/rosidl_typesupport_c__visibility_control.h"
#include "uav_car_interfaces/srv/detail/control_service__struct.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace uav_car_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _ControlService_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ControlService_Request_type_support_ids_t;

static const _ControlService_Request_type_support_ids_t _ControlService_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ControlService_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ControlService_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ControlService_Request_type_support_symbol_names_t _ControlService_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, srv, ControlService_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, uav_car_interfaces, srv, ControlService_Request)),
  }
};

typedef struct _ControlService_Request_type_support_data_t
{
  void * data[2];
} _ControlService_Request_type_support_data_t;

static _ControlService_Request_type_support_data_t _ControlService_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ControlService_Request_message_typesupport_map = {
  2,
  "uav_car_interfaces",
  &_ControlService_Request_message_typesupport_ids.typesupport_identifier[0],
  &_ControlService_Request_message_typesupport_symbol_names.symbol_name[0],
  &_ControlService_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ControlService_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ControlService_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace uav_car_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_C_EXPORT_uav_car_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, uav_car_interfaces, srv, ControlService_Request)() {
  return &::uav_car_interfaces::srv::rosidl_typesupport_c::ControlService_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "uav_car_interfaces/msg/rosidl_typesupport_c__visibility_control.h"
// already included above
// #include "uav_car_interfaces/srv/detail/control_service__struct.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace uav_car_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _ControlService_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ControlService_Response_type_support_ids_t;

static const _ControlService_Response_type_support_ids_t _ControlService_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ControlService_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ControlService_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ControlService_Response_type_support_symbol_names_t _ControlService_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, srv, ControlService_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, uav_car_interfaces, srv, ControlService_Response)),
  }
};

typedef struct _ControlService_Response_type_support_data_t
{
  void * data[2];
} _ControlService_Response_type_support_data_t;

static _ControlService_Response_type_support_data_t _ControlService_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ControlService_Response_message_typesupport_map = {
  2,
  "uav_car_interfaces",
  &_ControlService_Response_message_typesupport_ids.typesupport_identifier[0],
  &_ControlService_Response_message_typesupport_symbol_names.symbol_name[0],
  &_ControlService_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ControlService_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ControlService_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace uav_car_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_C_EXPORT_uav_car_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, uav_car_interfaces, srv, ControlService_Response)() {
  return &::uav_car_interfaces::srv::rosidl_typesupport_c::ControlService_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "uav_car_interfaces/msg/rosidl_typesupport_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace uav_car_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _ControlService_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ControlService_type_support_ids_t;

static const _ControlService_type_support_ids_t _ControlService_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ControlService_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ControlService_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ControlService_type_support_symbol_names_t _ControlService_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, uav_car_interfaces, srv, ControlService)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, uav_car_interfaces, srv, ControlService)),
  }
};

typedef struct _ControlService_type_support_data_t
{
  void * data[2];
} _ControlService_type_support_data_t;

static _ControlService_type_support_data_t _ControlService_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ControlService_service_typesupport_map = {
  2,
  "uav_car_interfaces",
  &_ControlService_service_typesupport_ids.typesupport_identifier[0],
  &_ControlService_service_typesupport_symbol_names.symbol_name[0],
  &_ControlService_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t ControlService_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ControlService_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace uav_car_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_C_EXPORT_uav_car_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, uav_car_interfaces, srv, ControlService)() {
  return &::uav_car_interfaces::srv::rosidl_typesupport_c::ControlService_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
