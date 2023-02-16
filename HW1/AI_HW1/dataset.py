import os
import cv2
import glob
def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """

    # Begin your code (Part 1)
    '''
    First, I use glob(x), which can see all files in x.
    Therfore, name will be dataPath+'face' then dataPath+'non-face'.
    variable j meaning classification will be 1 when we are reading images in 'face' 
    and be 0 otherwise. 
    Finally, we read every image in GRAYSCALE to let img.shape be (19,19,1).
    We put img and j together and return it
    '''
    images = []
    j=1
    aim=dataPath+'/*'
    for name in glob.glob(aim):
      #print ('\t', name)
      for filename in os.listdir(name):
            #print ('\t', filename)
            img = cv2.imread(os.path.join(name,filename),cv2.IMREAD_GRAYSCALE)
            if img is not None:
                #print(img[0])
                #print(img[0].shape)
                #print(img[:,:,0:0].shape)
                images.append((img,j))
      j=j-1
    return images
    # raise NotImplementedError("To be implemented")
    # End your code (Part 1)
    
    