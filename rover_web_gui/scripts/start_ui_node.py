#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This script reads parameters from rosparam server and creates a symbolic link
# to the urdf package directory, which is denoted by urdf_package_name parameter,
# in the 'packages' directory. Thus the web client can download the meshes that are
# defined in the URDF file.
#
import rospy
import roslib; roslib.load_manifest('rover_web_gui')
import os
import sys
import SimpleHTTPServer
import SocketServer
import signal
import threading

def signalHandler(signum, frame):
    rospy.loginfo("Itu Rover Web Client: shutting down")
    global http_server
    if not (http_server is None):
        http_server.shutdown()
        http_server.server_close()

    rospy.signal_shutdown("Interrupt or terminate signal received")
    global symlink_path
    if not (symlink_path is None):
        os.unlink(symlink_path)

def main():
    rospy.init_node("start_ui_node", disable_signals=True)
    # read the urdf_package_name parameter into variable: package_name
    package_name = ""
    if rospy.has_param("~urdf_package_name"):
        package_name = rospy.get_param("~urdf_package_name")
    else:
        rospy.logfatal("urdf_package_name parameter must be set!")
        sys.exit(1)

    # default port
    port = rospy.get_param("~port",default=8000)

    urdf_package_path = ""
    try:
        urdf_package_path = roslib.packages.get_pkg_dir(package_name)
    except:
        urdf_package_path = ""

    if urdf_package_path == "":
        rospy.logfatal("Package %s does not exist!" % (package_name))
        sys.exit(1)

    # Create the packages directory if it is not exist in the system
    tmp_path = "/tmp/itu_rover_web_client_tmp"
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    global symlink_path
    symlink_path = tmp_path + "/" + package_name
    if not os.path.exists(symlink_path):
        os.symlink(urdf_package_path,symlink_path)

    # Set signal handlers
    signal.signal(signal.SIGINT, signalHandler)
    signal.signal(signal.SIGTERM, signalHandler)

    # cd into src dir
    my_package_path = roslib.packages.get_pkg_dir("rover_web_gui")
    os.chdir(my_package_path + "/assets")
    # Run the web server!
    http_handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    global http_server
    http_server = SocketServer.TCPServer(("0.0.0.0", port), http_handler)
    http_thread = threading.Thread(target = http_server.serve_forever)
    http_thread.start()
    rospy.loginfo("Itu Rover Web Client: listening on port %d" % (port))

    # Main loop, waits 1 second to join then handles signals
    while True:
        http_thread.join(1)
        if not http_thread.is_alive():
            break

http_server = None
symlink_path = None
if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
