# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include".split(';') if "${prefix}/include" != "" else []
PROJECT_CATKIN_DEPENDS = "angles;nodelet;roscpp;roslib;sensor_msgs;tf;velodyne_driver;velodyne_msgs;dynamic_reconfigure;diagnostic_updater".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lvelodyne_rawdata".split(';') if "-lvelodyne_rawdata" != "" else []
PROJECT_NAME = "velodyne_pointcloud"
PROJECT_SPACE_DIR = "/home/basestation/rover20_ws/install"
PROJECT_VERSION = "1.5.2"
