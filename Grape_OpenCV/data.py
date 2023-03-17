import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def find_cluster(arr):
    sc = StandardScaler()
    arr_sc = sc.fit_transform(arr)
    #   KMeans
    km = KMeans(n_clusters=2) 
    km = km.fit(arr_sc)
    return arr_sc, km

def plot_cluster(arr):
    #   Find cluster
    arr_sc, km = find_cluster(arr)
    #   Center of cluster
    centroids = km.cluster_centers_
    plt.figure(figsize=(8, 6))
    for i in range(len(arr)):
        # plt.scatter(arr[i][0], arr[i][1], c = 'b' if km.labels_[i] == 0 else 'g')
        plt.scatter(arr[i][0], arr[i][1], c = 'b')
    plt.title("Center coordinates of grapes", c = 'g', fontsize=15, fontweight='bold')
    plt.xlabel("X", c = 'r', fontsize=15, fontweight='bold')
    plt.ylabel("Y", c = 'r', fontsize=15, fontweight='bold')
    plt.grid()
    plt.show()


if __name__ == "__main__":
    filenames = os.listdir("grape_data")
    plot_cluster(filenames)
    

# import sys
# import cv2
# import numpy as np


# cap1 = cv2.VideoCapture('videos/DBSCAN.mp4')
# cap2 = cv2.VideoCapture('videos/KMeans.mp4')

# out = cv2.VideoWriter('videos/final.mp4',cv2.VideoWriter_fourcc('M','J','P','G'))
  
# while(cap1.isOpened() and cap2.isOpened()):
#   ret1, frame1 = cap1.read()
#   frame1 = cv2.resize(frame1, dsize=None, fx=0.5, fy=0.5)
#   ret2, frame2 = cap2.read()
#   frame2 = cv2.resize(frame2, dsize=None, fx=0.5, fy=0.5)
#   if ret1 == True and ret2 == True: 
#     img_h = cv2.hconcat([frame2, frame1])

#     cv2.imshow("Concat Image", img_h)
#     out.write(img_h)
 
#     # Press Q on keyboard to  exit
#     if cv2.waitKey(23) & 0xFF == ord('q'):
#       break 
 
# cap1.release() 
# cap2.release() 
# cv2.destroyAllWindows()