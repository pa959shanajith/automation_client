import cv2
import numpy as np

def mask(image_path,coordinates):

    mask_img='masked.png'

    xmid=int((coordinates[2] + coordinates[0])/2)
    ymid=int((coordinates[3] + coordinates[1])/2)
    x_dist=int(xmid-coordinates[0])
    y_dist=int(ymid-coordinates[1])
    thickness=y_dist*2
    
    
    
    image = cv2.imread(image_path,0)
    mask = np.zeros(image.shape[:2], dtype="uint8")
    mask=cv2.rectangle(mask, (xmid-x_dist+3,ymid+2),(xmid+x_dist, ymid),color=(255, 255, 255), thickness=thickness)
    masked = cv2.bitwise_and(image, image, mask=mask)
    #masked = cv2.bitwise_or(image, mask)
    cv2.imwrite(mask_img,masked)
    return masked