# FaceF
A library for face recognition, flexible and easy to use. The library uses a lot of models like ssd, mtcnn, facenet .... These models will be downloaded automatically when used for the first time, please make sure your network connection is not blocked to google drive.

# Install
**FaceF** is available on [pypi.org](https://pypi.org/), if you just want to use it for your project, install it using pip.
Requires python>=3.6, tensorflow2
```
pip install facef
```
# To use
## 1. Face detection

```py
import cv2
from facef.detection import ssd_detect, mtcnn_detect 

img = cv2.imread('path_to_image.jpg')

boxes = ssd_detect(img)
# boxes,_ = mtcnn_detect(img)
for box in boxes:
    cv2.rectangle(img), (box[0],box[1]), (box[2],box[3]), (0,255,0),thickness=2)
cv2.imshow('image', img)
```

## 2. Face extract feature 

```py
import cv2
from facef.extraction import facenet_ext 

img_face = cv2.imread('face_image.jpg')

emb = facenet_ext(face_img)
print(emb)
```

## 3. Get face distance

```py
import cv2
from facef.distance import face2face_distance 

distance = face2face_distance(emb_face1, emb_face2)
print(distance)
```