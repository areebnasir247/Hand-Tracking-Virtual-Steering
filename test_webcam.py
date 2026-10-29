import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera not found!")
else:
    print("Webcam working! Press Q to exit.")

while camera.isOpened():
    success, frame = camera.read()

    if not success:
        break

    cv2.imshow("Virtual Steering Wheel - Webcam Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
