// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice
#include "uav_car_interfaces/msg/detail/image_processor_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
uav_car_interfaces__msg__ImageProcessorData__init(uav_car_interfaces__msg__ImageProcessorData * msg)
{
  if (!msg) {
    return false;
  }
  // res_x
  // res_y
  // res_flag
  return true;
}

void
uav_car_interfaces__msg__ImageProcessorData__fini(uav_car_interfaces__msg__ImageProcessorData * msg)
{
  if (!msg) {
    return;
  }
  // res_x
  // res_y
  // res_flag
}

bool
uav_car_interfaces__msg__ImageProcessorData__are_equal(const uav_car_interfaces__msg__ImageProcessorData * lhs, const uav_car_interfaces__msg__ImageProcessorData * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // res_x
  if (lhs->res_x != rhs->res_x) {
    return false;
  }
  // res_y
  if (lhs->res_y != rhs->res_y) {
    return false;
  }
  // res_flag
  if (lhs->res_flag != rhs->res_flag) {
    return false;
  }
  return true;
}

bool
uav_car_interfaces__msg__ImageProcessorData__copy(
  const uav_car_interfaces__msg__ImageProcessorData * input,
  uav_car_interfaces__msg__ImageProcessorData * output)
{
  if (!input || !output) {
    return false;
  }
  // res_x
  output->res_x = input->res_x;
  // res_y
  output->res_y = input->res_y;
  // res_flag
  output->res_flag = input->res_flag;
  return true;
}

uav_car_interfaces__msg__ImageProcessorData *
uav_car_interfaces__msg__ImageProcessorData__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__msg__ImageProcessorData * msg = (uav_car_interfaces__msg__ImageProcessorData *)allocator.allocate(sizeof(uav_car_interfaces__msg__ImageProcessorData), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(uav_car_interfaces__msg__ImageProcessorData));
  bool success = uav_car_interfaces__msg__ImageProcessorData__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
uav_car_interfaces__msg__ImageProcessorData__destroy(uav_car_interfaces__msg__ImageProcessorData * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    uav_car_interfaces__msg__ImageProcessorData__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
uav_car_interfaces__msg__ImageProcessorData__Sequence__init(uav_car_interfaces__msg__ImageProcessorData__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__msg__ImageProcessorData * data = NULL;

  if (size) {
    data = (uav_car_interfaces__msg__ImageProcessorData *)allocator.zero_allocate(size, sizeof(uav_car_interfaces__msg__ImageProcessorData), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = uav_car_interfaces__msg__ImageProcessorData__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        uav_car_interfaces__msg__ImageProcessorData__fini(&data[i - 1]);
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
uav_car_interfaces__msg__ImageProcessorData__Sequence__fini(uav_car_interfaces__msg__ImageProcessorData__Sequence * array)
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
      uav_car_interfaces__msg__ImageProcessorData__fini(&array->data[i]);
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

uav_car_interfaces__msg__ImageProcessorData__Sequence *
uav_car_interfaces__msg__ImageProcessorData__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__msg__ImageProcessorData__Sequence * array = (uav_car_interfaces__msg__ImageProcessorData__Sequence *)allocator.allocate(sizeof(uav_car_interfaces__msg__ImageProcessorData__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = uav_car_interfaces__msg__ImageProcessorData__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
uav_car_interfaces__msg__ImageProcessorData__Sequence__destroy(uav_car_interfaces__msg__ImageProcessorData__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    uav_car_interfaces__msg__ImageProcessorData__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
uav_car_interfaces__msg__ImageProcessorData__Sequence__are_equal(const uav_car_interfaces__msg__ImageProcessorData__Sequence * lhs, const uav_car_interfaces__msg__ImageProcessorData__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!uav_car_interfaces__msg__ImageProcessorData__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
uav_car_interfaces__msg__ImageProcessorData__Sequence__copy(
  const uav_car_interfaces__msg__ImageProcessorData__Sequence * input,
  uav_car_interfaces__msg__ImageProcessorData__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(uav_car_interfaces__msg__ImageProcessorData);
    uav_car_interfaces__msg__ImageProcessorData * data =
      (uav_car_interfaces__msg__ImageProcessorData *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!uav_car_interfaces__msg__ImageProcessorData__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          uav_car_interfaces__msg__ImageProcessorData__fini(&data[i]);
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
    if (!uav_car_interfaces__msg__ImageProcessorData__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
