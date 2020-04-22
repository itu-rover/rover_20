# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/usr/include;/usr/include/libusb-1.0".split(';') if "${prefix}/include;/usr/include;/usr/include/libusb-1.0" != "" else []
PROJECT_CATKIN_DEPENDS = "roscpp;sensor_msgs;diagnostic_updater;dynamic_reconfigure".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lsick_tim_3xx;/usr/lib/x86_64-linux-gnu/libboost_system.so;-lusb-1.0".split(';') if "-lsick_tim_3xx;/usr/lib/x86_64-linux-gnu/libboost_system.so;-lusb-1.0" != "" else []
PROJECT_NAME = "sick_tim"
PROJECT_SPACE_DIR = "/home/basestation/rover20_ws/install"
PROJECT_VERSION = "0.0.10"
