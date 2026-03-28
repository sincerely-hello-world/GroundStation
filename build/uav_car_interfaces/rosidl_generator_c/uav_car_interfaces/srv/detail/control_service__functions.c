// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from uav_car_interfaces:srv/ControlService.idl
// generated code does not contain a copyright notice
#include "uav_car_interfaces/srv/detail/control_service__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `req`
#include "rosidl_runtime_c/string_functions.h"

bool
uav_car_interfaces__srv__ControlService_Request__init(uav_car_interfaces__srv__ControlService_Request * msg)
{
  if (!msg) {
    return false;
  }
  // req
  if (!rosidl_runtime_c__String__init(&msg->req)) {
    uav_car_interfaces__srv__ControlService_Request__fini(msg);
    return false;
  }
  return true;
}

void
uav_car_interfaces__srv__ControlService_Request__fini(uav_car_interfaces__srv__ControlService_Request * msg)
{
  if (!msg) {
    return;
  }
  // req
  rosidl_runtime_c__String__fini(&msg->req);
}

bool
uav_car_interfaces__srv__ControlService_Request__are_equal(const uav_car_interfaces__srv__ControlService_Request * lhs, const uav_car_interfaces__srv__ControlService_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // req
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->req), &(rhs->req)))
  {
    return false;
  }
  return true;
}

bool
uav_car_interfaces__srv__ControlService_Request__copy(
  const uav_car_interfaces__srv__ControlService_Request * input,
  uav_car_interfaces__srv__ControlService_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // req
  if (!rosidl_runtime_c__String__copy(
      &(input->req), &(output->req)))
  {
    return false;
  }
  return true;
}

uav_car_interfaces__srv__ControlService_Request *
uav_car_interfaces__srv__ControlService_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__srv__ControlService_Request * msg = (uav_car_interfaces__srv__ControlService_Request *)allocator.allocate(sizeof(uav_car_interfaces__srv__ControlService_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(uav_car_interfaces__srv__ControlService_Request));
  bool success = uav_car_interfaces__srv__ControlService_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
uav_car_interfaces__srv__ControlService_Request__destroy(uav_car_interfaces__srv__ControlService_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    uav_car_interfaces__srv__ControlService_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
uav_car_interfaces__srv__ControlService_Request__Sequence__init(uav_car_interfaces__srv__ControlService_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__srv__ControlService_Request * data = NULL;

  if (size) {
    data = (uav_car_interfaces__srv__ControlService_Request *)allocator.zero_allocate(size, sizeof(uav_car_interfaces__srv__ControlService_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = uav_car_interfaces__srv__ControlService_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        uav_car_interfaces__srv__ControlService_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
uav_car_interfaces__srv__ControlService_Request__Sequence__fini(uav_car_interfaces__srv__ControlService_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      uav_car_interfaces__srv__ControlService_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

uav_car_interfaces__srv__ControlService_Request__Sequence *
uav_car_interfaces__srv__ControlService_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__srv__ControlService_Request__Sequence * array = (uav_car_interfaces__srv__ControlService_Request__Sequence *)allocator.allocate(sizeof(uav_car_interfaces__srv__ControlService_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = uav_car_interfaces__srv__ControlService_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
uav_car_interfaces__srv__ControlService_Request__Sequence__destroy(uav_car_interfaces__srv__ControlService_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    uav_car_interfaces__srv__ControlService_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
uav_car_interfaces__srv__ControlService_Request__Sequence__are_equal(const uav_car_interfaces__srv__ControlService_Request__Sequence * lhs, const uav_car_interfaces__srv__ControlService_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!uav_car_interfaces__srv__ControlService_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
uav_car_interfaces__srv__ControlService_Request__Sequence__copy(
  const uav_car_interfaces__srv__ControlService_Request__Sequence * input,
  uav_car_interfaces__srv__ControlService_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(uav_car_interfaces__srv__ControlService_Request);
    uav_car_interfaces__srv__ControlService_Request * data =
      (uav_car_interfaces__srv__ControlService_Request *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!uav_car_interfaces__srv__ControlService_Request__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          uav_car_interfaces__srv__ControlService_Request__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!uav_car_interfaces__srv__ControlService_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `echo`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
uav_car_interfaces__srv__ControlService_Response__init(uav_car_interfaces__srv__ControlService_Response * msg)
{
  if (!msg) {
    return false;
  }
  // echo
  if (!rosidl_runtime_c__String__init(&msg->echo)) {
    uav_car_interfaces__srv__ControlService_Response__fini(msg);
    return false;
  }
  return true;
}

void
uav_car_interfaces__srv__ControlService_Response__fini(uav_car_interfaces__srv__ControlService_Response * msg)
{
  if (!msg) {
    return;
  }
  // echo
  rosidl_runtime_c__String__fini(&msg->echo);
}

bool
uav_car_interfaces__srv__ControlService_Response__are_equal(const uav_car_interfaces__srv__ControlService_Response * lhs, const uav_car_interfaces__srv__ControlService_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // echo
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->echo), &(rhs->echo)))
  {
    return false;
  }
  return true;
}

bool
uav_car_interfaces__srv__ControlService_Response__copy(
  const uav_car_interfaces__srv__ControlService_Response * input,
  uav_car_interfaces__srv__ControlService_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // echo
  if (!rosidl_runtime_c__String__copy(
      &(input->echo), &(output->echo)))
  {
    return false;
  }
  return true;
}

uav_car_interfaces__srv__ControlService_Response *
uav_car_interfaces__srv__ControlService_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__srv__ControlService_Response * msg = (uav_car_interfaces__srv__ControlService_Response *)allocator.allocate(sizeof(uav_car_interfaces__srv__ControlService_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(uav_car_interfaces__srv__ControlService_Response));
  bool success = uav_car_interfaces__srv__ControlService_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
uav_car_interfaces__srv__ControlService_Response__destroy(uav_car_interfaces__srv__ControlService_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    uav_car_interfaces__srv__ControlService_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
uav_car_interfaces__srv__ControlService_Response__Sequence__init(uav_car_interfaces__srv__ControlService_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__srv__ControlService_Response * data = NULL;

  if (size) {
    data = (uav_car_interfaces__srv__ControlService_Response *)allocator.zero_allocate(size, sizeof(uav_car_interfaces__srv__ControlService_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = uav_car_interfaces__srv__ControlService_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        uav_car_interfaces__srv__ControlService_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
uav_car_interfaces__srv__ControlService_Response__Sequence__fini(uav_car_interfaces__srv__ControlService_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      uav_car_interfaces__srv__ControlService_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

uav_car_interfaces__srv__ControlService_Response__Sequence *
uav_car_interfaces__srv__ControlService_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__srv__ControlService_Response__Sequence * array = (uav_car_interfaces__srv__ControlService_Response__Sequence *)allocator.allocate(sizeof(uav_car_interfaces__srv__ControlService_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = uav_car_interfaces__srv__ControlService_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
uav_car_interfaces__srv__ControlService_Response__Sequence__destroy(uav_car_interfaces__srv__ControlService_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    uav_car_interfaces__srv__ControlService_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
uav_car_interfaces__srv__ControlService_Response__Sequence__are_equal(const uav_car_interfaces__srv__ControlService_Response__Sequence * lhs, const uav_car_interfaces__srv__ControlService_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!uav_car_interfaces__srv__ControlService_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
uav_car_interfaces__srv__ControlService_Response__Sequence__copy(
  const uav_car_interfaces__srv__ControlService_Response__Sequence * input,
  uav_car_interfaces__srv__ControlService_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(uav_car_interfaces__srv__ControlService_Response);
    uav_car_interfaces__srv__ControlService_Response * data =
      (uav_car_interfaces__srv__ControlService_Response *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!uav_car_interfaces__srv__ControlService_Response__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          uav_car_interfaces__srv__ControlService_Response__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!uav_car_interfaces__srv__ControlService_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
