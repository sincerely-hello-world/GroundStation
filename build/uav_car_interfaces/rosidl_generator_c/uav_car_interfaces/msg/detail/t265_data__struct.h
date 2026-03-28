// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from uav_car_interfaces:msg/T265Data.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__STRUCT_H_
#define UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/T265Data in the package uav_car_interfaces.
typedef struct uav_car_interfaces__msg__T265Data
{
  double pos_x;
  double pos_y;
  double pos_z;
  int64_t confidence;
  double tof_z;
} uav_car_interfaces__msg__T265Data;

// Struct for a sequence of uav_car_interfaces__msg__T265Data.
typedef struct uav_car_interfaces__msg__T265Data__Sequence
{
  uav_car_interfaces__msg__T265Data * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} uav_car_interfaces__msg__T265Data__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__STRUCT_H_
