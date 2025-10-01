import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Declare common variables
width = 1280
height = 720
folder_path = "pre_img"

# Camera settings
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
cap.set(3, width)
cap.set(4, height)

# Get list of images
pathImages = sorted(os.listdir(folder_path), key=len)
if not pathImages:
    print(f"Error: No images found in folder {folder_path}")
    exit()
print(f"Slides found: {pathImages}")

# Variables
imgNumber = 3
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = 0
annotationStart = False

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # Importing images
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from webcam.")
        break
    img = cv2.flip(img, 1)

    # Load the current slide
    pathFullImg = os.path.join(folder_path, pathImages[imgNumber])
    print(f"Loading slide: {pathFullImg}")
    imgCurrent = cv2.imread(pathFullImg)
    if imgCurrent is None:
        print(f"Error: Could not load image {pathFullImg}")
        break

    # Resize slide image to take 80% of the screen width
    slideWidth = int(width * 0.8)
    slideHeight = height
    imgCurrent = cv2.resize(imgCurrent, (slideWidth, slideHeight))

    # Resize webcam feed to take 20% of the screen width and 35% of the screen height
    webcamWidth = int(width * 0.2)
    webcamHeight = int(height * 0.35)
    imgSmall = cv2.resize(img, (webcamWidth, webcamHeight))

    # Create a blank canvas for the final layout
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # Place the slide image on the left (80% width)
    canvas[0:slideHeight, 0:slideWidth] = imgCurrent

    # Place the webcam feed on the bottom-right corner (20% width, 35% height)
    canvas[height - webcamHeight:height, slideWidth:width] = imgSmall

    # Add navigation details above the slide
    cv2.putText(canvas, "Navigation: [Left: Previous Slide] [Right: Next Slide] [Q: Quit]",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Hand detection
    hands, img = detector.findHands(img)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        # Check if the hand is inside the webcam feed area
        if slideWidth <= cx <= width and (height - webcamHeight) <= cy <= height:
            annotationStart = False

            # Gesture 1 - Left Slide
            if fingers == [1, 0, 0, 0, 0]:
                annotationStart = False
                print("Left Slide")
                if imgNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber -= 1

            # Gesture 2 - Right Slide
            if fingers == [0, 0, 0, 0, 1]:
                annotationStart = False
                print("Right Slide")
                if imgNumber < len(pathImages) - 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber += 1

    # Button press delay
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    # Draw annotations
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(canvas, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 8)

    # Display the final layout
    cv2.imshow("Presentation Viewer", canvas)

    # Manual quit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()