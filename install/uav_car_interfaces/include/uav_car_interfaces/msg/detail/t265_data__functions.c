// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from uav_car_interfaces:msg/T265Data.idl
// generated code does not contain a copyright notice
#include "uav_car_interfaces/msg/detail/t265_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
uav_car_interfaces__msg__T265Data__init(uav_car_interfaces__msg__T265Data * msg)
{
  if (!msg) {
    return false;
  }
  // pos_x
  // pos_y
  // pos_z
  // confidence
  return true;
}

void
uav_car_interfaces__msg__T265Data__fini(uav_car_interfaces__msg__T265Data * msg)
{
  if (!msg) {
    return;
  }
  // pos_x
  // pos_y
  // pos_z
  // confidence
}

bool
uav_car_interfaces__msg__T265Data__are_equal(const uav_car_interfaces__msg__T265Data * lhs, const uav_car_interfaces__msg__T265Data * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pos_x
  if (lhs->pos_x != rhs->pos_x) {
    return false;
  }
  // pos_y
  if (lhs->pos_y != rhs->pos_y) {
    return false;
  }
  // pos_z
  if (lhs->pos_z != rhs->pos_z) {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  return true;
}

bool
uav_car_interfaces__msg__T265Data__copy(
  const uav_car_interfaces__msg__T265Data * input,
  uav_car_interfaces__msg__T265Data * output)
{
  if (!input || !output) {
    return false;
  }
  // pos_x
  output->pos_x = input->pos_x;
  // pos_y
  output->pos_y = input->pos_y;
  // pos_z
  output->pos_z = input->pos_z;
  // confidence
  output->confidence = input->confidence;
  return true;
}

uav_car_interfaces__msg__T265Data *
uav_car_interfaces__msg__T265Data__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__msg__T265Data * msg = (uav_car_interfaces__msg__T265Data *)allocator.allocate(sizeof(uav_car_interfaces__msg__T265Data), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(uav_car_interfaces__msg__T265Data));
  bool success = uav_car_interfaces__msg__T265Data__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
uav_car_interfaces__msg__T265Data__destroy(uav_car_interfaces__msg__T265Data * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    uav_car_interfaces__msg__T265Data__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
uav_car_interfaces__msg__T265Data__Sequence__init(uav_car_interfaces__msg__T265Data__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__msg__T265Data * data = NULL;

  if (size) {
    data = (uav_car_interfaces__msg__T265Data *)allocator.zero_allocate(size, sizeof(uav_car_interfaces__msg__T265Data), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = uav_car_interfaces__msg__T265Data__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        uav_car_interfaces__msg__T265Data__fini(&data[i - 1]);
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
uav_car_interfaces__msg__T265Data__Sequence__fini(uav_car_interfaces__msg__T265Data__Sequence * array)
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
      uav_car_interfaces__msg__T265Data__fini(&array->data[i]);
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

uav_car_interfaces__msg__T265Data__Sequence *
uav_car_interfaces__msg__T265Data__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_car_interfaces__msg__T265Data__Sequence * array = (uav_car_interfaces__msg__T265Data__Sequence *)allocator.allocate(sizeof(uav_car_interfaces__msg__T265Data__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = uav_car_interfaces__msg__T265Data__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
uav_car_interfaces__msg__T265Data__Sequence__destroy(uav_car_interfaces__msg__T265Data__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    uav_car_interfaces__msg__T265Data__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
uav_car_interfaces__msg__T265Data__Sequence__are_equal(const uav_car_interfaces__msg__T265Data__Sequence * lhs, const uav_car_interfaces__msg__T265Data__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!uav_car_interfaces__msg__T265Data__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
uav_car_interfaces__msg__T265Data__Sequence__copy(
  const uav_car_interfaces__msg__T265Data__Sequence * input,
  uav_car_interfaces__msg__T265Data__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(uav_car_interfaces__msg__T265Data);
    uav_car_interfaces__msg__T265Data * data =
      (uav_car_interfaces__msg__T265Data *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!uav_car_interfaces__msg__T265Data__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          uav_car_interfaces__msg__T265Data__fini(&data[i]);
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
    if (!uav_car_interfaces__msg__T265Data__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
