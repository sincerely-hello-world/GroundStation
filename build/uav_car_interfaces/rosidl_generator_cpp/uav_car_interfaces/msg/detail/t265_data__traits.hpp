// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from uav_car_interfaces:msg/T265Data.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__TRAITS_HPP_
#define UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__TRAITS_HPP_

#include "uav_car_interfaces/msg/detail/t265_data__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<uav_car_interfaces::msg::T265Data>()
{
  return "uav_car_interfaces::msg::T265Data";
}

template<>
inline const char * name<uav_car_interfaces::msg::T265Data>()
{
  return "uav_car_interfaces/msg/T265Data";
}

template<>
struct has_fixed_size<uav_car_interfaces::msg::T265Data>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<uav_car_interfaces::msg::T265Data>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<uav_car_interfaces::msg::T265Data>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__TRAITS_HPP_
