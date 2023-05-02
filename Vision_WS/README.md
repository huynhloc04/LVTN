# **This implementation is an instruction for grape detection using Deep Learning method: YOLOv5s and optimizes post-training model by TensorRT**

## **Why YOLOv5s**

![github image](https://github.com/huynhloc04/LVTN/blob/main/Vision_WS/images/YOLO_Compare.jpg)

As two graphs showed above, on left side is the relationship of the number of parameters and mAP on COCO dataset and the right one is between latency and mAP.

For the purpose of deploying to edge devices (Jetson Nano), we need a lightweight model to optimize the hardware. So, "nano", "tiny" or "small" would be the best choices.

After a process of repeated testing, we realized that YOLOv5s performed very well on Jetson Nano. The others also performed pretty well but they have a trade-off between performance and latency. So YOLOv5s is the best choice in a scenario of an edge device (Jetson Nano B01).

>> **Our model can detect all grapes on the tree and classify them as green or ripe. So that robot can distinguish and only harvest ripe ones.**

### **Image below is the flowchart of robot**

![github image](https://github.com/huynhloc04/LVTN/blob/main/Vision_WS/images/flowchart.jpg)

## **Training**

- Dataset used: [thsant/wgisd](https://zenodo.org/record/3361736#.XcQJVzMzZPY) + images collected from the Internet and labeled by Roboflow
- Download [GrapeTrain_YOLOv5.ipynb](https://github.com/huynhloc04/LVTN/blob/main/Vision_WS/GrpeTrain_YOLOv5.ipynb) file and run notebook cells. It will automatically install all requirement packages and download data from Robofow for training.
- I have trained my own on [kaggle.com](https://www.kaggle.com/)
  
  
***Note:***  *change the following parameters to config argument*

```bash
python train.py --img 640 --batch-size 128 --epochs 300 --data {dataset.location}/data.yaml --weights yolov5n.pt
                                       64                                                             yolov5s
                                       40                                                             yolov5m
                                       24                                                             yolov5l
                                       16                                                             yolov5x

  --img: input image size, default: 640 (640x640)
  --batch: number of batch size
  --epoch: number of epoch
  --data: data config file
  --weights: type of pre-trained model
```

***Make sure you read all of this before training:*** [Tips for Best Training Results](https://github.com/ultralytics/yolov5/wiki/Tips-for-Best-Training-Results)


## **TensorRT for deployment**

This session is all of instructions for converting trained model to **TensorRT** - an SDK for high-performance deep learning inference. 

For more information about TensorRT, visit here: https://developer.nvidia.com/tensorrt

***Note:*** 
- All of the following implementations are directly performed on Jetson Nano. 
- This instruction is only for the **YOLOv5s** and aims to reproduce my results. You can try the others by visiting: *https://github.com/wang-xinyu/tensorrtx*


#### **Convert YOLOv5s to TensorRT**

- #### I. Requirements

    TensorRT 7.x

- #### II. Conversion 
    
    **1. Download a couple of the following repo:**

    From home directory, for yolov5 v6.2, 
    - `git clone -b v6.2 https://github.com/ultralytics/yolov5.git` 
    
    and

    - `git clone -b yolov5-v6.2 https://github.com/wang-xinyu/tensorrtx.git`
  
  ####

    **2. Configuration**
  - Choose the model n/s/m/l/x/n6/s6/m6/l6/x6 from command line arguments.
  - Input shape defined in yololayer.h
  - Number of classes defined in yololayer.h, **DO NOT FORGET TO ADAPT THIS, If using your own model**
  - FP16/FP32 can be selected by the macro in yolov5.cpp
  - NMS thresh in yolov5.cpp
  - BBox confidence thresh in yolov5.cpp
  - Batch size in yolov5.cpp

  ####

    **3. Build and run**

    3.1 Generate .wts from pytorch with .pt, or download .wts from model zoo

    ```bash
    cp {tensorrtx}/yolov5/gen_wts.py {ultralytics}/yolov5
    cd {ultralytics}/yolov5
    python gen_wts.py -w yolov5s.pt -o yolov5s.wts
    // a file 'yolov5s.wts' will be generated.
    ```

    3.2 Build tensorrtx/yolov5

    ```bash
    cd {tensorrtx}/yolov5/
    // update CLASS_NUM in yololayer.h if your model is trained on custom dataset
    mkdir build
    cd build
    cp {ultralytics}/yolov5/yolov5s.wts {tensorrtx}/yolov5/build
    cmake ..
    make
    sudo ./yolov5 -s [.wts] [.engine] s  // serialize model to plan file
    ```

    After convert and serialize, ".so" and ".engine" file is generated.
    
    **4. Benchmark results**
    
    The following table summarizes how different models perform on Jetson Nano B01.
    
<!--     ![github image](https://github.com/huynhloc04/LVTN/blob/main/Vision_WS/images/benchmark.jpg) -->
    <img src="https://github.com/huynhloc04/LVTN/blob/main/Vision_WS/images/benchmark.jpg" width=50% height=50%>
    

    #####

    **Demo video:** *https://www.youtube.com/watch?v=FpePov3S0_M*

    #####

    3.3 Run converted model and integrate with **Robot Operating System (ROS)**.

    Clone [Vision_WS](https://github.com/huynhloc04/LVTN/tree/main/Vision_WS) to your directory and copy two generated files above to [src](https://github.com/huynhloc04/LVTN/tree/main/Vision_WS/src/lvtn_pkg/src) folder.

    - Open your terminal, type: ```roscore```
    - Open the second terminal or press **Ctrl + Shift + T**, type: ```rosrun vision_pkg pub_track.py```. This is to initialze rosnode: **OD** and rostopic: **vision**. So, the TensorRT model is run and publishes a message contains coordinate **(X, Y, Z)** to **vision** topic.
    Do not forget to source the bash file before run these line of code: ```source devel/setup.bash```

    - Optional: To see what pub_track.py publishes to **vision** topic, open the next terminal and type: ```rostopic echo vision```
  ######
   
   The content of a message is published would be as follow:
   
   ![github image](https://github.com/huynhloc04/LVTN/blob/main/Vision_WS/images/message.jpg)

    ```bash
    X: coordinate of grape along the X axis
    Y: coordinate of grape along the Y axis
    Z: coordinate of grape along the Z axis
    classID: type of grapes: green or ripe; 0 is green, 1 is ripe
    ```

    This coordinates will be used to control robot for grape harvesting task.
    
    ## **Results and demonstrations**
    
    **Detected results:**
    
    ![github image](https://github.com/huynhloc04/LVTN/blob/main/images/result.jpg)
        
    **Demo video:** *https://www.youtube.com/watch?v=5mz9hTh2y6E&t=16s*




 

    





  

  





