import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    
    # Begin your code (Part 4)
    """
    from line 31 to line 37, I read the txt into text[].
    variable t is to record when to break the loop, means no data to read.
    path is the name of the image, num represents how many face to detect.
    from line 42 to line 57, I record the location of faces.
    from line 58 to line 60, I cut the region and resize them.
    And I use f=[] to record whether the region is detected to be face or not.
    Finally, according to f=[], i put red/green box on image.
    PS: Why (t>len(text)-1) because text will read ' ' at the end.
    """
    text=[]
    t=0
    with open(dataPath) as f:
        tmp = f.read()
        list = tmp.split('\n')
        for i in list:
            text.append(i)
    #print(text)
    while (1):
        if(t>=len(text)-1):
            break
        list=text[t].split(' ')
        path=list[0]
        num=list[1]
        img = cv2.imread('data/detect/'+path,cv2.IMREAD_GRAYSCALE)
        t=t+1
        y=[]
        x=[]
        h=[]
        w=[]
        f=[]
        for j in range(int(num)):
            list=text[t+j].split(' ')
            y.append(int(list[0]))
            x.append(int(list[1]))
            h.append(int(list[2]))
            w.append(int(list[3]))
            crop_img = img[x[j]:x[j]+w[j], y[j]:y[j]+h[j]]
            dsize=(19,19)
            output = cv2.resize(crop_img, dsize)
            f.append(clf.classify(output))
            #plt.imshow(output,cmap='gray')
            #plt.show()
        
        #fig, ax = plt.subplots()
        img2 = cv2.imread('data/detect/'+path)
        #plt.imshow(img2)
        #plt.show()
        for j in range(len(f)):
            if f[j]==1:
                cv2.rectangle(img2,(y[j],x[j]),(y[j]+w[j],x[j]+h[j]),(0,255,0),3,cv2.LINE_AA)
            else:
                cv2.rectangle(img2,(y[j],x[j]),(y[j]+w[j],x[j]+h[j]),(0,0,255),3,cv2.LINE_AA)
        plt.imshow(img2[:,:,::-1])
        plt.show()
        t=t+int(num)
    
    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)
