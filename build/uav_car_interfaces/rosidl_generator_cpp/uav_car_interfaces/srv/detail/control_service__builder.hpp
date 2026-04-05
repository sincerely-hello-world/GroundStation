// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from uav_car_interfaces:srv/ControlService.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__BUILDER_HPP_
#define UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__BUILDER_HPP_

#include "uav_car_interfaces/srv/detail/control_service__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace uav_car_interfaces
{

namespace srv
{

namespace builder
{

class Init_ControlService_Request_req
{
public:
  Init_ControlService_Request_req()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::uav_car_interfaces::srv::ControlService_Request req(::uav_car_interfaces::srv::ControlService_Request::_req_type arg)
  {
    msg_.req = std::move(arg);
    return std::move(msg_);
  }

private:
  ::uav_car_interfaces::srv::ControlService_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::uav_car_interfaces::srv::ControlService_Request>()
{
  return uav_car_interfaces::srv::builder::Init_ControlService_Request_req();
}

}  // namespace uav_car_interfaces


namespace uav_car_interfaces
{

namespace srv
{

namespace builder
{

class Init_ControlService_Response_echo
{
public:
  Init_ControlService_Response_echo()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::uav_car_interfaces::srv::ControlService_Response echo(::uav_car_interfaces::srv::ControlService_Response::_echo_type arg)
  {
    msg_.echo = std::move(arg);
    return std::move(msg_);
  }

private:
  ::uav_car_interfaces::srv::ControlService_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::uav_car_interfaces::srv::ControlService_Response>()
{
  return uav_car_interfaces::srv::builder::Init_ControlService_Response_echo();
}

}  // namespace uav_car_interfaces

#endif  // UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__BUILDER_HPP_
