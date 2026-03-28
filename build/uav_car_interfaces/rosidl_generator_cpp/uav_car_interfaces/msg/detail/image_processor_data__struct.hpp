// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__STRUCT_HPP_
#define UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__uav_car_interfaces__msg__ImageProcessorData __attribute__((deprecated))
#else
# define DEPRECATED__uav_car_interfaces__msg__ImageProcessorData __declspec(deprecated)
#endif

namespace uav_car_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ImageProcessorData_
{
  using Type = ImageProcessorData_<ContainerAllocator>;

  explicit ImageProcessorData_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->res_x = 0;
      this->res_y = 0;
      this->res_flag = 0;
    }
  }

  explicit ImageProcessorData_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->res_x = 0;
      this->res_y = 0;
      this->res_flag = 0;
    }
  }

  // field types and members
  using _res_x_type =
    int8_t;
  _res_x_type res_x;
  using _res_y_type =
    int8_t;
  _res_y_type res_y;
  using _res_flag_type =
    int8_t;
  _res_flag_type res_flag;

  // setters for named parameter idiom
  Type & set__res_x(
    const int8_t & _arg)
  {
    this->res_x = _arg;
    return *this;
  }
  Type & set__res_y(
    const int8_t & _arg)
  {
    this->res_y = _arg;
    return *this;
  }
  Type & set__res_flag(
    const int8_t & _arg)
  {
    this->res_flag = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator> *;
  using ConstRawPtr =
    const uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__uav_car_interfaces__msg__ImageProcessorData
    std::shared_ptr<uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__uav_car_interfaces__msg__ImageProcessorData
    std::shared_ptr<uav_car_interfaces::msg::ImageProcessorData_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ImageProcessorData_ & other) const
  {
    if (this->res_x != other.res_x) {
      return false;
    }
    if (this->res_y != other.res_y) {
      return false;
    }
    if (this->res_flag != other.res_flag) {
      return false;
    }
    return true;
  }
  bool operator!=(const ImageProcessorData_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ImageProcessorData_

// alias to use template instance with default allocator
using ImageProcessorData =
  uav_car_interfaces::msg::ImageProcessorData_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace uav_car_interfaces

#endif  // UAV_CAR_INTERFACES__MSG__DETAIL__IMAGE_PROCESSOR_DATA__STRUCT_HPP_
