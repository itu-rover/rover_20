
(cl:in-package :asdf)

(defsystem "rover20_state_mach-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "StateMsg" :depends-on ("_package_StateMsg"))
    (:file "_package_StateMsg" :depends-on ("_package"))
  ))