# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "rover_20_control: 1 messages, 0 services")

set(MSG_I_FLAGS "-Irover_20_control:/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(rover_20_control_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg" NAME_WE)
add_custom_target(_rover_20_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rover_20_control" "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(rover_20_control
  "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rover_20_control
)

### Generating Services

### Generating Module File
_generate_module_cpp(rover_20_control
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rover_20_control
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(rover_20_control_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(rover_20_control_generate_messages rover_20_control_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg" NAME_WE)
add_dependencies(rover_20_control_generate_messages_cpp _rover_20_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rover_20_control_gencpp)
add_dependencies(rover_20_control_gencpp rover_20_control_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rover_20_control_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(rover_20_control
  "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rover_20_control
)

### Generating Services

### Generating Module File
_generate_module_eus(rover_20_control
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rover_20_control
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(rover_20_control_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(rover_20_control_generate_messages rover_20_control_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg" NAME_WE)
add_dependencies(rover_20_control_generate_messages_eus _rover_20_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rover_20_control_geneus)
add_dependencies(rover_20_control_geneus rover_20_control_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rover_20_control_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(rover_20_control
  "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rover_20_control
)

### Generating Services

### Generating Module File
_generate_module_lisp(rover_20_control
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rover_20_control
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(rover_20_control_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(rover_20_control_generate_messages rover_20_control_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg" NAME_WE)
add_dependencies(rover_20_control_generate_messages_lisp _rover_20_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rover_20_control_genlisp)
add_dependencies(rover_20_control_genlisp rover_20_control_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rover_20_control_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(rover_20_control
  "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rover_20_control
)

### Generating Services

### Generating Module File
_generate_module_nodejs(rover_20_control
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rover_20_control
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(rover_20_control_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(rover_20_control_generate_messages rover_20_control_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg" NAME_WE)
add_dependencies(rover_20_control_generate_messages_nodejs _rover_20_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rover_20_control_gennodejs)
add_dependencies(rover_20_control_gennodejs rover_20_control_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rover_20_control_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(rover_20_control
  "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rover_20_control
)

### Generating Services

### Generating Module File
_generate_module_py(rover_20_control
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rover_20_control
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(rover_20_control_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(rover_20_control_generate_messages rover_20_control_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/basestation/rover20_ws/src/rover_20/rover_20_control/msg/Arm_msgs.msg" NAME_WE)
add_dependencies(rover_20_control_generate_messages_py _rover_20_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rover_20_control_genpy)
add_dependencies(rover_20_control_genpy rover_20_control_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rover_20_control_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rover_20_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rover_20_control
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rover_20_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rover_20_control
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rover_20_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rover_20_control
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rover_20_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rover_20_control
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rover_20_control)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rover_20_control\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rover_20_control
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
