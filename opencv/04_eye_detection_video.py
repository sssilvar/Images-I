import cv2

# Create a capture object (from video)
cap = cv2.VideoCapture('C:\Users\Smith\Downloads\GOPR0303.MP4')

# Create a Haar cascade
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

# Start processing!
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # Resize frame
        frame = cv2.resize(frame, (853, 480))
        # Convert frame to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in eyes:
            frame = cv2.rectangle(frame, (x,y), (x+h, y+w), (0, 255, 0), 2)

        # Vizualise image
        cv2.imshow('Eye Segmentation', frame)

    # Check for interruption
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close and release everything
cap.release()
cv2.destroyAllWindows()
