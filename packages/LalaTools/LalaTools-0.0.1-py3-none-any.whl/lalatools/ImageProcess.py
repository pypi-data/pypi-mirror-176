import cv2
import numpy as np
from mss import mss

class match_process():
    
    def __init__(self,large_image,small_image):
        try: self.large_image = cv2.imread(large_image) # Read the images from the file
        except: self.large_image = large_image
        try: self.small_image = cv2.imread(small_image) # Read the images from the file
        except: self.small_image = small_image
        
        method = cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(self.small_image, self.large_image, method)
        self.mn,_,self.mnLoc,_ = cv2.minMaxLoc(result) # min_val, max_val, min_loc, max_loc
        self.MPx,self.MPy = self.mnLoc
        self.trows,self.tcols = self.small_image.shape[:2]
    
    def judge(self,min=0.02):
        if(self.mn<min): return True
        else: return False
        
    def drawRect(self):
        cv2.rectangle(self.large_image, (self.MPx,self.MPy),(self.MPx+self.tcols,self.MPy+self.trows),(0,0,255),2)
        cv2.imwrite('match.png',self.large_image) #cv2.imshow('match',large_image), cv2.waitKey(0)
    
    def value(self):# center_pos, xywh, min_value
        return (int(self.MPx+self.tcols/2), int(self.MPy+self.trows/2)), (self.MPx, self.MPy, self.trows, self.tcols), self.mn

def Match(large_image,small_image,min=0.02):
    """
    compare two images, check match or not.
    :param min: Criteria
    :param return: False or ( (center-x, center-y), (left, top, w, h), eval_min_val )
    """
    mp = match_process(large_image,small_image)
    if(mp.judge(min)):
        return mp.value()
    else:
        return False
    
def MatchWithImage(large_image,small_image,min=0.02):
    """
    compare two images, check match or not.
    :param min: Criteria
    :param return: False or ( (center-x, center-y), (left-x, left-y, w, h), eval_min_val )
    generate result as 'match.png'
    """
    
    mp = match_process(large_image,small_image)
    if(mp.judge(min)):
        mp.drawRect()
        return mp.value()
    else:
        return False
    
def ScreenCapture(left=0, top=0, width=300, height=300):
    bounding_box = {'top': top, 'left': left, 'width': width, 'height': height}
    img = np.array(mss().grab(bounding_box))
    return img

def Test_Screen(left=0, top=0, width=300, height=300):
    while True:
        cv2.imshow('screen', ScreenCapture(left, top, width, height))
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break