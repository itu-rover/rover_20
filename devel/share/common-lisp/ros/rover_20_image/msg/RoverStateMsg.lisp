; Auto-generated. Do not edit!


(cl:in-package rover_20_image-msg)


;//! \htmlinclude RoverStateMsg.msg.html

(cl:defclass <RoverStateMsg> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (state
    :reader state
    :initarg :state
    :type cl:integer
    :initform 0))
)

(cl:defclass RoverStateMsg (<RoverStateMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RoverStateMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RoverStateMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rover_20_image-msg:<RoverStateMsg> is deprecated: use rover_20_image-msg:RoverStateMsg instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <RoverStateMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_20_image-msg:header-val is deprecated.  Use rover_20_image-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'state-val :lambda-list '(m))
(cl:defmethod state-val ((m <RoverStateMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_20_image-msg:state-val is deprecated.  Use rover_20_image-msg:state instead.")
  (state m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<RoverStateMsg>)))
    "Constants for message type '<RoverStateMsg>"
  '((:INITIALISE . 0)
    (:READY . 1)
    (:REACH_GPS . 2)
    (:FIND_IMAGE . 3)
    (:REACH_IMAGE . 4)
    (:DEINITIALISE . 5)
    (:ERROR . 6))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'RoverStateMsg)))
    "Constants for message type 'RoverStateMsg"
  '((:INITIALISE . 0)
    (:READY . 1)
    (:REACH_GPS . 2)
    (:FIND_IMAGE . 3)
    (:REACH_IMAGE . 4)
    (:DEINITIALISE . 5)
    (:ERROR . 6))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RoverStateMsg>) ostream)
  "Serializes a message object of type '<RoverStateMsg>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'state)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RoverStateMsg>) istream)
  "Deserializes a message object of type '<RoverStateMsg>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'state)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RoverStateMsg>)))
  "Returns string type for a message object of type '<RoverStateMsg>"
  "rover_20_image/RoverStateMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RoverStateMsg)))
  "Returns string type for a message object of type 'RoverStateMsg"
  "rover_20_image/RoverStateMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RoverStateMsg>)))
  "Returns md5sum for a message object of type '<RoverStateMsg>"
  "7c5823584edb2f28d14ea0a2b593dda6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RoverStateMsg)))
  "Returns md5sum for a message object of type 'RoverStateMsg"
  "7c5823584edb2f28d14ea0a2b593dda6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RoverStateMsg>)))
  "Returns full string definition for message of type '<RoverStateMsg>"
  (cl:format cl:nil "std_msgs/Header header~%~%byte INITIALISE = 0~%byte READY = 1~%byte REACH_GPS = 2~%byte FIND_IMAGE = 3~%byte REACH_IMAGE = 4~%byte DEINITIALISE = 5~%byte ERROR = 6~%~%byte state~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RoverStateMsg)))
  "Returns full string definition for message of type 'RoverStateMsg"
  (cl:format cl:nil "std_msgs/Header header~%~%byte INITIALISE = 0~%byte READY = 1~%byte REACH_GPS = 2~%byte FIND_IMAGE = 3~%byte REACH_IMAGE = 4~%byte DEINITIALISE = 5~%byte ERROR = 6~%~%byte state~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RoverStateMsg>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RoverStateMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'RoverStateMsg
    (cl:cons ':header (header msg))
    (cl:cons ':state (state msg))
))
