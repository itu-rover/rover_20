;; Auto-generated. Do not edit!


(when (boundp 'rover20_state_mach::StateMsg)
  (if (not (find-package "ROVER20_STATE_MACH"))
    (make-package "ROVER20_STATE_MACH"))
  (shadow 'StateMsg (find-package "ROVER20_STATE_MACH")))
(unless (find-package "ROVER20_STATE_MACH::STATEMSG")
  (make-package "ROVER20_STATE_MACH::STATEMSG"))

(in-package "ROS")
;;//! \htmlinclude StateMsg.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(intern "*INITIALISE*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*INITIALISE* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*INITIALISE* 0)
(intern "*READY*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*READY* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*READY* 1)
(intern "*REACH_GPS*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*REACH_GPS* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*REACH_GPS* 2)
(intern "*FIND_ARTAG*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*FIND_ARTAG* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*FIND_ARTAG* 3)
(intern "*REACH_ARTAG*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*REACH_ARTAG* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*REACH_ARTAG* 4)
(intern "*APPROACH*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*APPROACH* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*APPROACH* 5)
(intern "*PASS_GATE*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*PASS_GATE* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*PASS_GATE* 6)
(intern "*DEINITIALISE*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*DEINITIALISE* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*DEINITIALISE* 7)
(intern "*ERROR*" (find-package "ROVER20_STATE_MACH::STATEMSG"))
(shadow '*ERROR* (find-package "ROVER20_STATE_MACH::STATEMSG"))
(defconstant rover20_state_mach::StateMsg::*ERROR* 8)
(defclass rover20_state_mach::StateMsg
  :super ros::object
  :slots (_header _state ))

(defmethod rover20_state_mach::StateMsg
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:state __state) 0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _state (round __state))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; byte _state
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; byte _state
       (write-byte _state s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; byte _state
     (setq _state (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _state 127) (setq _state (- _state 256)))
   ;;
   self)
  )

(setf (get rover20_state_mach::StateMsg :md5sum-) "bb3cba5455b3506b2a8435bf0f050c07")
(setf (get rover20_state_mach::StateMsg :datatype-) "rover20_state_mach/StateMsg")
(setf (get rover20_state_mach::StateMsg :definition-)
      "std_msgs/Header header

byte INITIALISE = 0
byte READY = 1
byte REACH_GPS = 2
byte FIND_ARTAG = 3
byte REACH_ARTAG = 4
byte APPROACH = 5
byte PASS_GATE = 6
byte DEINITIALISE = 7
byte ERROR = 8


byte state

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

")



(provide :rover20_state_mach/StateMsg "bb3cba5455b3506b2a8435bf0f050c07")


