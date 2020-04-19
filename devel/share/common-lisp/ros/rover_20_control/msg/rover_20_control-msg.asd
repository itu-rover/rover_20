
(cl:in-package :asdf)

(defsystem "rover_20_control-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Arm_msgs" :depends-on ("_package_Arm_msgs"))
    (:file "_package_Arm_msgs" :depends-on ("_package"))
  ))