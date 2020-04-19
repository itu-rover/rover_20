
(cl:in-package :asdf)

(defsystem "rover_20_image-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "RoverStateMsg" :depends-on ("_package_RoverStateMsg"))
    (:file "_package_RoverStateMsg" :depends-on ("_package"))
  ))