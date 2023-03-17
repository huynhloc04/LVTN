import sys
import cv2
import numpy as np
from data import find_cluster
from data import plot_cluster
import matplotlib.pyplot as plt

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('videos/KMeans.avi', fourcc, 5, (1344, 756))

def show_hist(arr):   
  #   Data pre-processing
  plt.hist(arr[:, 0], len(arr), density=True)
  plt.xlabel("X coordinate")
  plt.ylabel("Count")
  plt.show()
   

cap = cv2.VideoCapture('grape_2.mp4')
  
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True: 
    # Display the resulting frame
    frame = cv2.resize(frame, dsize=None, fx=0.7, fy=0.7)
    print(frame.shape)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     
    gray = cv2.medianBlur(gray, 5)      
    rows, cloms = gray.shape[:2]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50,
                               param1=15, param2=20,
                               minRadius=15, maxRadius=30)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))[0]
        
        arr_sc, km = find_cluster(circles)
        centroids = km.cluster_centers_

        cluster_1 = circles[km.labels_==0]
        cluster_2 = circles[km.labels_==1]

        clusters = (cluster_1, cluster_2)
        # =============== Circle only ================
        # for i in cluster_1:
        #     center = (i[0], i[1])
        #     radius = i[2]
        #     cv2.circle(frame, center, radius, (0, 0, 255), 2) 
        # for i in cluster_2:
        #      center = (i[0], i[1])
        #      radius = i[2]
        #      cv2.circle(frame, center, radius, (0, 0, 255), 2) 

        # =============== Bounding box only ================
        # for cluster in clusters:
        #   x1, y1 = np.min(cluster, axis=0)[:2]
        #   r1 = cluster[cluster[:, 0]==x1][0][-1]
        #   x2, y2 = np.max(cluster, axis=0)[:2]
        #   r2 = cluster[cluster[:, 0]==x2][0][-1]
        #   cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 0, 255), 2)

        # =============== Bounding box + Circle ================
        # for i in cluster_1:
        #     center = (i[0], i[1])
        #     radius = i[2]
        #     cv2.circle(frame, center, radius, (0, 0, 255), 2) 
        #     cv2.circle(frame, center, 7, (0, 0, 0), -1) 
        #     x1, y1 = np.min(cluster_1, axis=0)[:2]
        #     r1 = cluster_1[cluster_1[:, 0]==x1][0][-1]
        #     x2, y2 = np.max(cluster_1, axis=0)[:2]
        #     r2 = cluster_1[cluster_1[:, 0]==x2][0][-1]
        #     cv2.rectangle(frame, (x1-r1, y1-r1), (x2+r2, y2+r2), (0, 0, 255), 2)            
        # for i in cluster_2:
        #     center = (i[0], i[1])
        #     radius = i[2]
        #     cv2.circle(frame, center, radius, (255, 0, 0), 2)   
        #     cv2.circle(frame, center, 7, (0, 0, 0), -1) 
        #     x1, y1 = np.min(cluster_2, axis=0)[:2]
        #     r1 = cluster_2[cluster_2[:, 0]==x1][0][-1]
        #     x2, y2 = np.max(cluster_2, axis=0)[:2]
        #     r2 = cluster_2[cluster_2[:, 0]==x2][0][-1]
        #     cv2.rectangle(frame, (x1-r1, y1-r1), (x2+r2, y2+r2), (255, 0, 0), 2)     
    
    cv2.imshow("Grape", frame)
    out.write(frame)
    # plot_cluster(circles)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(23) & 0xFF == ord('q'):
      break 
 
cap.release() 
cv2.destroyAllWindows()


# import cv2
# import numpy as np
  
# # Read image.
# img = cv2.imread('grape.jpg', cv2.IMREAD_COLOR)
# img = cv2.resize(img, dsize=None, fx=0.5, fy=0.5)
  
# # Convert to grayscale.
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# # Blur using 3 * 3 kernel.
# gray_blurred = cv2.blur(gray, (3, 3))
  
# # Apply Hough transform on the blurred image.
# detected_circles = cv2.HoughCircles(gray_blurred, 
#                    cv2.HOUGH_GRADIENT, 1, 10, param1 = 10,
#                param2 = 35, minRadius = 10, maxRadius = 50)
  
  
# # Convert the circle parameters a, b and r to integers.
# detected_circles = np.uint16(np.around(detected_circles))
    
# for circle in detected_circles[0]:
#     a, b, r = circle[0], circle[1], circle[2]
  
#     # Draw the circumference of the circle.
#     cv2.circle(img, (a, b), r, (0, 255, 0), 2)
# cv2.imshow("Detected Circle", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
