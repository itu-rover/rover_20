;; Auto-generated. Do not edit!


(when (boundp 'rover_20_image::RoverStateMsg)
  (if (not (find-package "ROVER_20_IMAGE"))
    (make-package "ROVER_20_IMAGE"))
  (shadow 'RoverStateMsg (find-package "ROVER_20_IMAGE")))
(unless (find-package "ROVER_20_IMAGE::ROVERSTATEMSG")
  (make-package "ROVER_20_IMAGE::ROVERSTATEMSG"))

(in-package "ROS")
;;//! \htmlinclude RoverStateMsg.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(intern "*INITIALISE*" (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(shadow '*INITIALISE* (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(defconstant rover_20_image::RoverStateMsg::*INITIALISE* 0)
(intern "*READY*" (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(shadow '*READY* (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(defconstant rover_20_image::RoverStateMsg::*READY* 1)
(intern "*REACH_GPS*" (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(shadow '*REACH_GPS* (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(defconstant rover_20_image::RoverStateMsg::*REACH_GPS* 2)
(intern "*FIND_IMAGE*" (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(shadow '*FIND_IMAGE* (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(defconstant rover_20_image::RoverStateMsg::*FIND_IMAGE* 3)
(intern "*REACH_IMAGE*" (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(shadow '*REACH_IMAGE* (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(defconstant rover_20_image::RoverStateMsg::*REACH_IMAGE* 4)
(intern "*DEINITIALISE*" (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(shadow '*DEINITIALISE* (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(defconstant rover_20_image::RoverStateMsg::*DEINITIALISE* 5)
(intern "*ERROR*" (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(shadow '*ERROR* (find-package "ROVER_20_IMAGE::ROVERSTATEMSG"))
(defconstant rover_20_image::RoverStateMsg::*ERROR* 6)
(defclass rover_20_image::RoverStateMsg
  :super ros::object
  :slots (_header _state ))

(defmethod rover_20_image::RoverStateMsg
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

(setf (get rover_20_image::RoverStateMsg :md5sum-) "7c5823584edb2f28d14ea0a2b593dda6")
(setf (get rover_20_image::RoverStateMsg :datatype-) "rover_20_image/RoverStateMsg")
(setf (get rover_20_image::RoverStateMsg :definition-)
      "std_msgs/Header header

byte INITIALISE = 0
byte READY = 1
byte REACH_GPS = 2
byte FIND_IMAGE = 3
byte REACH_IMAGE = 4
byte DEINITIALISE = 5
byte ERROR = 6

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



(provide :rover_20_image/RoverStateMsg "7c5823584edb2f28d14ea0a2b593dda6")


