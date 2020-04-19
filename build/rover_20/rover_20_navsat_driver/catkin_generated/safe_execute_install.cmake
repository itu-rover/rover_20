execute_process(COMMAND "/home/basestation/rover20_ws/build/rover_20/rover_20_navsat_driver/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/basestation/rover20_ws/build/rover_20/rover_20_navsat_driver/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
