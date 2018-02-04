import numpy as np
import cv2

# Define a capture object (webcam)
cap = cv2.VideoCapture(0)

# Define Haar classifier
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

while True:
    # Capture frame
    ret, frame = cap.read()

    # Convert to BW
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in eyes:
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow('Eyes', frame)

    # Wait for key command
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close and release all
cap.release()
cv2.destroyAllWindows()
