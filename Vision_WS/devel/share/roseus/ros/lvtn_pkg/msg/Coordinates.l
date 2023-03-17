;; Auto-generated. Do not edit!


(when (boundp 'lvtn_pkg::Coordinates)
  (if (not (find-package "LVTN_PKG"))
    (make-package "LVTN_PKG"))
  (shadow 'Coordinates (find-package "LVTN_PKG")))
(unless (find-package "LVTN_PKG::COORDINATES")
  (make-package "LVTN_PKG::COORDINATES"))

(in-package "ROS")
;;//! \htmlinclude Coordinates.msg.html


(defclass lvtn_pkg::Coordinates
  :super ros::object
  :slots (_x _y _d ))

(defmethod lvtn_pkg::Coordinates
  (:init
   (&key
    ((:x __x) 0)
    ((:y __y) 0)
    ((:d __d) 0.0)
    )
   (send-super :init)
   (setq _x (round __x))
   (setq _y (round __y))
   (setq _d (float __d))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:d
   (&optional __d)
   (if __d (setq _d __d)) _d)
  (:serialization-length
   ()
   (+
    ;; int16 _x
    2
    ;; int16 _y
    2
    ;; float32 _d
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _x
       (write-word _x s)
     ;; int16 _y
       (write-word _y s)
     ;; float32 _d
       (sys::poke _d (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _x
     (setq _x (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _y
     (setq _y (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; float32 _d
     (setq _d (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get lvtn_pkg::Coordinates :md5sum-) "b79627109fef5e4034006638adf0655d")
(setf (get lvtn_pkg::Coordinates :datatype-) "lvtn_pkg/Coordinates")
(setf (get lvtn_pkg::Coordinates :definition-)
      "int16 x
int16 y
float32 d

")



(provide :lvtn_pkg/Coordinates "b79627109fef5e4034006638adf0655d")


