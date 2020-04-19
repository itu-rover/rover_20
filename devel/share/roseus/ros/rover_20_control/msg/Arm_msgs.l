;; Auto-generated. Do not edit!


(when (boundp 'rover_20_control::Arm_msgs)
  (if (not (find-package "ROVER_20_CONTROL"))
    (make-package "ROVER_20_CONTROL"))
  (shadow 'Arm_msgs (find-package "ROVER_20_CONTROL")))
(unless (find-package "ROVER_20_CONTROL::ARM_MSGS")
  (make-package "ROVER_20_CONTROL::ARM_MSGS"))

(in-package "ROS")
;;//! \htmlinclude Arm_msgs.msg.html


(defclass rover_20_control::Arm_msgs
  :super ros::object
  :slots (_joint0 _joint1 _joint2 _joint3 _joint4 _joint5 _joint6 ))

(defmethod rover_20_control::Arm_msgs
  (:init
   (&key
    ((:joint0 __joint0) 0.0)
    ((:joint1 __joint1) 0.0)
    ((:joint2 __joint2) 0.0)
    ((:joint3 __joint3) 0.0)
    ((:joint4 __joint4) 0.0)
    ((:joint5 __joint5) 0.0)
    ((:joint6 __joint6) 0.0)
    )
   (send-super :init)
   (setq _joint0 (float __joint0))
   (setq _joint1 (float __joint1))
   (setq _joint2 (float __joint2))
   (setq _joint3 (float __joint3))
   (setq _joint4 (float __joint4))
   (setq _joint5 (float __joint5))
   (setq _joint6 (float __joint6))
   self)
  (:joint0
   (&optional __joint0)
   (if __joint0 (setq _joint0 __joint0)) _joint0)
  (:joint1
   (&optional __joint1)
   (if __joint1 (setq _joint1 __joint1)) _joint1)
  (:joint2
   (&optional __joint2)
   (if __joint2 (setq _joint2 __joint2)) _joint2)
  (:joint3
   (&optional __joint3)
   (if __joint3 (setq _joint3 __joint3)) _joint3)
  (:joint4
   (&optional __joint4)
   (if __joint4 (setq _joint4 __joint4)) _joint4)
  (:joint5
   (&optional __joint5)
   (if __joint5 (setq _joint5 __joint5)) _joint5)
  (:joint6
   (&optional __joint6)
   (if __joint6 (setq _joint6 __joint6)) _joint6)
  (:serialization-length
   ()
   (+
    ;; float64 _joint0
    8
    ;; float64 _joint1
    8
    ;; float64 _joint2
    8
    ;; float64 _joint3
    8
    ;; float64 _joint4
    8
    ;; float64 _joint5
    8
    ;; float64 _joint6
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _joint0
       (sys::poke _joint0 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _joint1
       (sys::poke _joint1 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _joint2
       (sys::poke _joint2 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _joint3
       (sys::poke _joint3 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _joint4
       (sys::poke _joint4 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _joint5
       (sys::poke _joint5 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _joint6
       (sys::poke _joint6 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _joint0
     (setq _joint0 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _joint1
     (setq _joint1 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _joint2
     (setq _joint2 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _joint3
     (setq _joint3 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _joint4
     (setq _joint4 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _joint5
     (setq _joint5 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _joint6
     (setq _joint6 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get rover_20_control::Arm_msgs :md5sum-) "4515360d2b590c5a38f3e5678e7e9266")
(setf (get rover_20_control::Arm_msgs :datatype-) "rover_20_control/Arm_msgs")
(setf (get rover_20_control::Arm_msgs :definition-)
      "float64  joint0
float64 joint1
float64 joint2
float64  joint3
float64  joint4
float64  joint5
float64  joint6

")



(provide :rover_20_control/Arm_msgs "4515360d2b590c5a38f3e5678e7e9266")


