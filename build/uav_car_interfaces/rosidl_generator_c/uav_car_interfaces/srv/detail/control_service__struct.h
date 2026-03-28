// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from uav_car_interfaces:srv/ControlService.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__STRUCT_H_
#define UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'req'
#include "rosidl_runtime_c/string.h"

// Struct defined in srv/ControlService in the package uav_car_interfaces.
typedef struct uav_car_interfaces__srv__ControlService_Request
{
  rosidl_runtime_c__String req;
} uav_car_interfaces__srv__ControlService_Request;

// Struct for a sequence of uav_car_interfaces__srv__ControlService_Request.
typedef struct uav_car_interfaces__srv__ControlService_Request__Sequence
{
  uav_car_interfaces__srv__ControlService_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} uav_car_interfaces__srv__ControlService_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'echo'
// already included above
// #include "rosidl_runtime_c/string.h"

// Struct defined in srv/ControlService in the package uav_car_interfaces.
typedef struct uav_car_interfaces__srv__ControlService_Response
{
  rosidl_runtime_c__String echo;
} uav_car_interfaces__srv__ControlService_Response;

// Struct for a sequence of uav_car_interfaces__srv__ControlService_Response.
typedef struct uav_car_interfaces__srv__ControlService_Response__Sequence
{
  uav_car_interfaces__srv__ControlService_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} uav_car_interfaces__srv__ControlService_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__STRUCT_H_
