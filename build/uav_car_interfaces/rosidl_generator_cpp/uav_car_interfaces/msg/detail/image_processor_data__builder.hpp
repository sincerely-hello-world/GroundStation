// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__BUILDER_HPP_
#define UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__BUILDER_HPP_

#include "uav_car_interfaces/msg/detail/image_processor_data__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace uav_car_interfaces
{

namespace msg
{

namespace builder
{

class Init_ImageProcessorData_res_flag
{
public:
  explicit Init_ImageProcessorData_res_flag(::uav_car_interfaces::msg::ImageProcessorData & msg)
  : msg_(msg)
  {}
  ::uav_car_interfaces::msg::ImageProcessorData res_flag(::uav_car_interfaces::msg::ImageProcessorData::_res_flag_type arg)
  {
    msg_.res_flag = std::move(arg);
    return std::move(msg_);
  }

private:
  ::uav_car_interfaces::msg::ImageProcessorData msg_;
};

class Init_ImageProcessorData_res_y
{
public:
  explicit Init_ImageProcessorData_res_y(::uav_car_interfaces::msg::ImageProcessorData & msg)
  : msg_(msg)
  {}
  Init_ImageProcessorData_res_flag res_y(::uav_car_interfaces::msg::ImageProcessorData::_res_y_type arg)
  {
    msg_.res_y = std::move(arg);
    return Init_ImageProcessorData_res_flag(msg_);
  }

private:
  ::uav_car_interfaces::msg::ImageProcessorData msg_;
};

class Init_ImageProcessorData_res_x
{
public:
  Init_ImageProcessorData_res_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ImageProcessorData_res_y res_x(::uav_car_interfaces::msg::ImageProcessorData::_res_x_type arg)
  {
    msg_.res_x = std::move(arg);
    return Init_ImageProcessorData_res_y(msg_);
  }

private:
  ::uav_car_interfaces::msg::ImageProcessorData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::uav_car_interfaces::msg::ImageProcessorData>()
{
  return uav_car_interfaces::msg::builder::Init_ImageProcessorData_res_x();
}

}  // namespace uav_car_interfaces

#endif  // UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__BUILDER_HPP_
