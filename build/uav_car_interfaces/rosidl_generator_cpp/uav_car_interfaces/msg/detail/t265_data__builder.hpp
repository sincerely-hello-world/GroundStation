// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from uav_car_interfaces:msg/T265Data.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__BUILDER_HPP_
#define UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__BUILDER_HPP_

#include "uav_car_interfaces/msg/detail/t265_data__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace uav_car_interfaces
{

namespace msg
{

namespace builder
{

class Init_T265Data_tof_z
{
public:
  explicit Init_T265Data_tof_z(::uav_car_interfaces::msg::T265Data & msg)
  : msg_(msg)
  {}
  ::uav_car_interfaces::msg::T265Data tof_z(::uav_car_interfaces::msg::T265Data::_tof_z_type arg)
  {
    msg_.tof_z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::uav_car_interfaces::msg::T265Data msg_;
};

class Init_T265Data_confidence
{
public:
  explicit Init_T265Data_confidence(::uav_car_interfaces::msg::T265Data & msg)
  : msg_(msg)
  {}
  Init_T265Data_tof_z confidence(::uav_car_interfaces::msg::T265Data::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_T265Data_tof_z(msg_);
  }

private:
  ::uav_car_interfaces::msg::T265Data msg_;
};

class Init_T265Data_pos_z
{
public:
  explicit Init_T265Data_pos_z(::uav_car_interfaces::msg::T265Data & msg)
  : msg_(msg)
  {}
  Init_T265Data_confidence pos_z(::uav_car_interfaces::msg::T265Data::_pos_z_type arg)
  {
    msg_.pos_z = std::move(arg);
    return Init_T265Data_confidence(msg_);
  }

private:
  ::uav_car_interfaces::msg::T265Data msg_;
};

class Init_T265Data_pos_y
{
public:
  explicit Init_T265Data_pos_y(::uav_car_interfaces::msg::T265Data & msg)
  : msg_(msg)
  {}
  Init_T265Data_pos_z pos_y(::uav_car_interfaces::msg::T265Data::_pos_y_type arg)
  {
    msg_.pos_y = std::move(arg);
    return Init_T265Data_pos_z(msg_);
  }

private:
  ::uav_car_interfaces::msg::T265Data msg_;
};

class Init_T265Data_pos_x
{
public:
  Init_T265Data_pos_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_T265Data_pos_y pos_x(::uav_car_interfaces::msg::T265Data::_pos_x_type arg)
  {
    msg_.pos_x = std::move(arg);
    return Init_T265Data_pos_y(msg_);
  }

private:
  ::uav_car_interfaces::msg::T265Data msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::uav_car_interfaces::msg::T265Data>()
{
  return uav_car_interfaces::msg::builder::Init_T265Data_pos_x();
}

}  // namespace uav_car_interfaces

#endif  // UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__BUILDER_HPP_
