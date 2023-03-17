import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

out = cv2.VideoWriter('videos/DBSCAN.mp4', cv2.VideoWriter_fourcc('M','J','P','G'), 5, (1344, 756))

cap = cv2.VideoCapture('grape_2.mp4')

def viz(circles, y_pred):
    plt.figure(figsize=(8, 6))
    plt.scatter(circles[:, 0], circles[:, 1], c=y_pred)        
    plt.title("Center coordinates of grapes", c = 'g', fontsize=15, fontweight='bold')
    plt.xlabel("X", c = 'r', fontsize=15, fontweight='bold')
    plt.ylabel("Y", c = 'r', fontsize=15, fontweight='bold')
    plt.grid()
    plt.show()

  
colors = [(255, 0, 0), 
          (0, 255, 0), 
          (0, 0, 255), 
          (255, 255, 0), 
          (0, 255, 255), 
          (255, 0, 255)]

while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True: 
    # Display the resulting frame
    frame = cv2.resize(frame, dsize=None, fx=0.7, fy=0.7)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     
    gray = cv2.medianBlur(gray, 5)      
    rows, cloms = gray.shape[:2]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50,
                               param1=15, param2=20,
                               minRadius=15, maxRadius=30)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))[0]
        sc_arr = StandardScaler().fit_transform(circles[:, :2])

        #   DBSCAN
        db = DBSCAN(eps=0.7, min_samples=7)
        db.fit(sc_arr)
        y_preds = db.fit_predict(sc_arr)

        # viz(circles, y_preds)       
         
        uni_preds = np.unique(y_preds) 
        color_c = np.random.choice(len(colors), len(uni_preds)-1, replace=False)
        for idx, pred in enumerate(uni_preds):
            if pred != -1:
                #   Draw circles
                for pts in circles[y_preds==pred]:
                   cv2.circle(frame, (pts[0], pts[1]), pts[2], colors[idx], 2)
                   cv2.circle(frame, (pts[0], pts[1]), 7, (0, 0, 0), -1)
                #   Draw bounding box
                cluster = circles[y_preds==pred]
                x1, y1 = np.min(cluster, axis=0)[:2]
                r1 = cluster[cluster[:, 0]==x1][0][-1]
                x2, y2 = np.max(cluster, axis=0)[:2]
                r2 = cluster[cluster[:, 0]==x2][0][-1]
                cv2.rectangle(frame, (x1-r1,y1-r1), (x2+r2,y2+r2), colors[idx], 2)
    
    cv2.imshow("Grape", frame)
    out.write(frame)
    # viz(circles, y_preds)                      
 
    # Press "q" on keyboard to exit
    if cv2.waitKey(23) & 0xFF == ord('q'):
      break 
 
cap.release() 
cv2.destroyAllWindows()

