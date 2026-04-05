// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__STRUCT_H_
#define UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/ImageProcessorData in the package uav_car_interfaces.
typedef struct uav_car_interfaces__msg__ImageProcessorData
{
  int8_t res_x;
  int8_t res_y;
  int8_t res_flag;
} uav_car_interfaces__msg__ImageProcessorData;

// Struct for a sequence of uav_car_interfaces__msg__ImageProcessorData.
typedef struct uav_car_interfaces__msg__ImageProcessorData__Sequence
{
  uav_car_interfaces__msg__ImageProcessorData * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} uav_car_interfaces__msg__ImageProcessorData__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__STRUCT_H_
