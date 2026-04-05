// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from uav_car_interfaces:srv/ControlService.idl
// generated code does not contain a copyright notice

#ifndef UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__STRUCT_HPP_
#define UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__uav_car_interfaces__srv__ControlService_Request __attribute__((deprecated))
#else
# define DEPRECATED__uav_car_interfaces__srv__ControlService_Request __declspec(deprecated)
#endif

namespace uav_car_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ControlService_Request_
{
  using Type = ControlService_Request_<ContainerAllocator>;

  explicit ControlService_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->req = "";
    }
  }

  explicit ControlService_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : req(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->req = "";
    }
  }

  // field types and members
  using _req_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _req_type req;

  // setters for named parameter idiom
  Type & set__req(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->req = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__uav_car_interfaces__srv__ControlService_Request
    std::shared_ptr<uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__uav_car_interfaces__srv__ControlService_Request
    std::shared_ptr<uav_car_interfaces::srv::ControlService_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControlService_Request_ & other) const
  {
    if (this->req != other.req) {
      return false;
    }
    return true;
  }
  bool operator!=(const ControlService_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ControlService_Request_

// alias to use template instance with default allocator
using ControlService_Request =
  uav_car_interfaces::srv::ControlService_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace uav_car_interfaces


#ifndef _WIN32
# define DEPRECATED__uav_car_interfaces__srv__ControlService_Response __attribute__((deprecated))
#else
# define DEPRECATED__uav_car_interfaces__srv__ControlService_Response __declspec(deprecated)
#endif

namespace uav_car_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ControlService_Response_
{
  using Type = ControlService_Response_<ContainerAllocator>;

  explicit ControlService_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->echo = "";
    }
  }

  explicit ControlService_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : echo(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->echo = "";
    }
  }

  // field types and members
  using _echo_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _echo_type echo;

  // setters for named parameter idiom
  Type & set__echo(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->echo = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__uav_car_interfaces__srv__ControlService_Response
    std::shared_ptr<uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__uav_car_interfaces__srv__ControlService_Response
    std::shared_ptr<uav_car_interfaces::srv::ControlService_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControlService_Response_ & other) const
  {
    if (this->echo != other.echo) {
      return false;
    }
    return true;
  }
  bool operator!=(const ControlService_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ControlService_Response_

// alias to use template instance with default allocator
using ControlService_Response =
  uav_car_interfaces::srv::ControlService_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace uav_car_interfaces

namespace uav_car_interfaces
{

namespace srv
{

struct ControlService
{
  using Request = uav_car_interfaces::srv::ControlService_Request;
  using Response = uav_car_interfaces::srv::ControlService_Response;
};

}  // namespace srv

}  // namespace uav_car_interfaces

#endif  // UAV_CAR_INTERFACES__SRV__DETAIL__CONTROL_SERVICE__STRUCT_HPP_
