// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from uav_car_interfaces:msg/T265Data.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__STRUCT_HPP_
#define UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__uav_car_interfaces__msg__T265Data __attribute__((deprecated))
#else
# define DEPRECATED__uav_car_interfaces__msg__T265Data __declspec(deprecated)
#endif

namespace uav_car_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct T265Data_
{
  using Type = T265Data_<ContainerAllocator>;

  explicit T265Data_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->pos_x = 0.0;
      this->pos_y = 0.0;
      this->pos_z = 0.0;
      this->confidence = 0ll;
      this->tof_z = 0.0;
    }
  }

  explicit T265Data_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->pos_x = 0.0;
      this->pos_y = 0.0;
      this->pos_z = 0.0;
      this->confidence = 0ll;
      this->tof_z = 0.0;
    }
  }

  // field types and members
  using _pos_x_type =
    double;
  _pos_x_type pos_x;
  using _pos_y_type =
    double;
  _pos_y_type pos_y;
  using _pos_z_type =
    double;
  _pos_z_type pos_z;
  using _confidence_type =
    int64_t;
  _confidence_type confidence;
  using _tof_z_type =
    double;
  _tof_z_type tof_z;

  // setters for named parameter idiom
  Type & set__pos_x(
    const double & _arg)
  {
    this->pos_x = _arg;
    return *this;
  }
  Type & set__pos_y(
    const double & _arg)
  {
    this->pos_y = _arg;
    return *this;
  }
  Type & set__pos_z(
    const double & _arg)
  {
    this->pos_z = _arg;
    return *this;
  }
  Type & set__confidence(
    const int64_t & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__tof_z(
    const double & _arg)
  {
    this->tof_z = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    uav_car_interfaces::msg::T265Data_<ContainerAllocator> *;
  using ConstRawPtr =
    const uav_car_interfaces::msg::T265Data_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<uav_car_interfaces::msg::T265Data_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<uav_car_interfaces::msg::T265Data_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      uav_car_interfaces::msg::T265Data_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<uav_car_interfaces::msg::T265Data_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      uav_car_interfaces::msg::T265Data_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<uav_car_interfaces::msg::T265Data_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<uav_car_interfaces::msg::T265Data_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<uav_car_interfaces::msg::T265Data_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__uav_car_interfaces__msg__T265Data
    std::shared_ptr<uav_car_interfaces::msg::T265Data_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__uav_car_interfaces__msg__T265Data
    std::shared_ptr<uav_car_interfaces::msg::T265Data_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const T265Data_ & other) const
  {
    if (this->pos_x != other.pos_x) {
      return false;
    }
    if (this->pos_y != other.pos_y) {
      return false;
    }
    if (this->pos_z != other.pos_z) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->tof_z != other.tof_z) {
      return false;
    }
    return true;
  }
  bool operator!=(const T265Data_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct T265Data_

// alias to use template instance with default allocator
using T265Data =
  uav_car_interfaces::msg::T265Data_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace uav_car_interfaces

#endif  // UAV_CAR_INTERFACES__MSG__DETAIL__T265_DATA__STRUCT_HPP_
