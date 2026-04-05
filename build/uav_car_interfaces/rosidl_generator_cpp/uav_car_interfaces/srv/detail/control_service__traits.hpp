// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from uav_car_interfaces:srv/ControlService.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__TRAITS_HPP_
#define UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__TRAITS_HPP_

#include "uav_car_interfaces/srv/detail/control_service__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<uav_car_interfaces::srv::ControlService_Request>()
{
  return "uav_car_interfaces::srv::ControlService_Request";
}

template<>
inline const char * name<uav_car_interfaces::srv::ControlService_Request>()
{
  return "uav_car_interfaces/srv/ControlService_Request";
}

template<>
struct has_fixed_size<uav_car_interfaces::srv::ControlService_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<uav_car_interfaces::srv::ControlService_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<uav_car_interfaces::srv::ControlService_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<uav_car_interfaces::srv::ControlService_Response>()
{
  return "uav_car_interfaces::srv::ControlService_Response";
}

template<>
inline const char * name<uav_car_interfaces::srv::ControlService_Response>()
{
  return "uav_car_interfaces/srv/ControlService_Response";
}

template<>
struct has_fixed_size<uav_car_interfaces::srv::ControlService_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<uav_car_interfaces::srv::ControlService_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<uav_car_interfaces::srv::ControlService_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<uav_car_interfaces::srv::ControlService>()
{
  return "uav_car_interfaces::srv::ControlService";
}

template<>
inline const char * name<uav_car_interfaces::srv::ControlService>()
{
  return "uav_car_interfaces/srv/ControlService";
}

template<>
struct has_fixed_size<uav_car_interfaces::srv::ControlService>
  : std::integral_constant<
    bool,
    has_fixed_size<uav_car_interfaces::srv::ControlService_Request>::value &&
    has_fixed_size<uav_car_interfaces::srv::ControlService_Response>::value
  >
{
};

template<>
struct has_bounded_size<uav_car_interfaces::srv::ControlService>
  : std::integral_constant<
    bool,
    has_bounded_size<uav_car_interfaces::srv::ControlService_Request>::value &&
    has_bounded_size<uav_car_interfaces::srv::ControlService_Response>::value
  >
{
};

template<>
struct is_service<uav_car_interfaces::srv::ControlService>
  : std::true_type
{
};

template<>
struct is_service_request<uav_car_interfaces::srv::ControlService_Request>
  : std::true_type
{
};

template<>
struct is_service_response<uav_car_interfaces::srv::ControlService_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__TRAITS_HPP_
