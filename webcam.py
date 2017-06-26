import numpy as np
import cv2
import helpers


cap = cv2.VideoCapture(0)
index = 0 


while(True):
   
    ret, frame = cap.read()
    cv2.imwrite('capture/img%04d.jpg' % index , frame)

    gray,thresh = helpers.detectTriangles(frame)
    index +=1

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()