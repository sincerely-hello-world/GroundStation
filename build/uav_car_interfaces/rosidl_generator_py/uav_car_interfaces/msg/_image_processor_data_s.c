// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from uav_car_interfaces:msg/ImageProcessorData.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "uav_car_interfaces/msg/detail/image_processor_data__struct.h"
#include "uav_car_interfaces/msg/detail/image_processor_data__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool uav_car_interfaces__msg__image_processor_data__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[64];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("uav_car_interfaces.msg._image_processor_data.ImageProcessorData", full_classname_dest, 63) == 0);
  }
  uav_car_interfaces__msg__ImageProcessorData * ros_message = _ros_message;
  {  // res_x
    PyObject * field = PyObject_GetAttrString(_pymsg, "res_x");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->res_x = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // res_y
    PyObject * field = PyObject_GetAttrString(_pymsg, "res_y");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->res_y = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // res_flag
    PyObject * field = PyObject_GetAttrString(_pymsg, "res_flag");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->res_flag = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * uav_car_interfaces__msg__image_processor_data__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of ImageProcessorData */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("uav_car_interfaces.msg._image_processor_data");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "ImageProcessorData");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  uav_car_interfaces__msg__ImageProcessorData * ros_message = (uav_car_interfaces__msg__ImageProcessorData *)raw_ros_message;
  {  // res_x
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->res_x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "res_x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // res_y
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->res_y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "res_y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // res_flag
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->res_flag);
    {
      int rc = PyObject_SetAttrString(_pymessage, "res_flag", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
