; Auto-generated. Do not edit!


(cl:in-package rover20_state_mach-msg)


;//! \htmlinclude StateMsg.msg.html

(cl:defclass <StateMsg> (roslisp-msg-protocol:ros-message)
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

(cl:defclass StateMsg (<StateMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <StateMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'StateMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rover20_state_mach-msg:<StateMsg> is deprecated: use rover20_state_mach-msg:StateMsg instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <StateMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover20_state_mach-msg:header-val is deprecated.  Use rover20_state_mach-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'state-val :lambda-list '(m))
(cl:defmethod state-val ((m <StateMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover20_state_mach-msg:state-val is deprecated.  Use rover20_state_mach-msg:state instead.")
  (state m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<StateMsg>)))
    "Constants for message type '<StateMsg>"
  '((:INITIALISE . 0)
    (:READY . 1)
    (:REACH_GPS . 2)
    (:FIND_ARTAG . 3)
    (:REACH_ARTAG . 4)
    (:APPROACH . 5)
    (:PASS_GATE . 6)
    (:DEINITIALISE . 7)
    (:ERROR . 8))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'StateMsg)))
    "Constants for message type 'StateMsg"
  '((:INITIALISE . 0)
    (:READY . 1)
    (:REACH_GPS . 2)
    (:FIND_ARTAG . 3)
    (:REACH_ARTAG . 4)
    (:APPROACH . 5)
    (:PASS_GATE . 6)
    (:DEINITIALISE . 7)
    (:ERROR . 8))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <StateMsg>) ostream)
  "Serializes a message object of type '<StateMsg>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'state)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <StateMsg>) istream)
  "Deserializes a message object of type '<StateMsg>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'state)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<StateMsg>)))
  "Returns string type for a message object of type '<StateMsg>"
  "rover20_state_mach/StateMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StateMsg)))
  "Returns string type for a message object of type 'StateMsg"
  "rover20_state_mach/StateMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<StateMsg>)))
  "Returns md5sum for a message object of type '<StateMsg>"
  "bb3cba5455b3506b2a8435bf0f050c07")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'StateMsg)))
  "Returns md5sum for a message object of type 'StateMsg"
  "bb3cba5455b3506b2a8435bf0f050c07")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<StateMsg>)))
  "Returns full string definition for message of type '<StateMsg>"
  (cl:format cl:nil "std_msgs/Header header~%~%byte INITIALISE = 0~%byte READY = 1~%byte REACH_GPS = 2~%byte FIND_ARTAG = 3~%byte REACH_ARTAG = 4~%byte APPROACH = 5~%byte PASS_GATE = 6~%byte DEINITIALISE = 7~%byte ERROR = 8~%~%~%byte state~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'StateMsg)))
  "Returns full string definition for message of type 'StateMsg"
  (cl:format cl:nil "std_msgs/Header header~%~%byte INITIALISE = 0~%byte READY = 1~%byte REACH_GPS = 2~%byte FIND_ARTAG = 3~%byte REACH_ARTAG = 4~%byte APPROACH = 5~%byte PASS_GATE = 6~%byte DEINITIALISE = 7~%byte ERROR = 8~%~%~%byte state~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <StateMsg>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <StateMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'StateMsg
    (cl:cons ':header (header msg))
    (cl:cons ':state (state msg))
))
