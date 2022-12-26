import cv2
import numpy as np

# HW8.3: Create a bird's eye view video from a fixed camera using perspective transformation and save it to a file, adding an annotation

circles = np.zeros((4, 2), np.int32)
counter = 0


def draw_circle(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        circles[counter] = x, y
        counter += 1
        cv2.circle(picArea, (x, y), 3, (255, 255, 0), -1)
        print(circles)


picArea = cv2.imread('footage.png')

while True:

    cv2.imshow('orig', picArea)
    cv2.setMouseCallback('orig', draw_circle)

    if counter == 4:
        height, width = picArea.shape[:2]
        pts1 = np.float32([circles[0], circles[1], circles[2], circles[3]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgOut = cv2.warpPerspective(picArea, matrix, (width, height))
        cv2.imshow("Out", imgOut)
        cv2.imwrite("perspective_road.png", imgOut)

    k = cv2.waitKey(20) & 0xFF  # stop on ESC and start video!
    if k == 27:
        break
cv2.destroyAllWindows()

video = cv2.VideoCapture('footage.mp4')
if not video.isOpened():
    print("error openning")
else:
    fps = video.get(5)
    print('fps:', fps)

    frame_count = video.get(7)
    print('Frame count:', frame_count)

while video.isOpened():
    ret, currentFrame = video.read()
    if ret:
        if counter == 4:
            height, width = currentFrame.shape[:2]
            pts1 = np.float32([circles[0], circles[1], circles[2], circles[3]])
            pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgOut = cv2.warpPerspective(currentFrame, matrix, (width, height))
            cv2.imshow("Out", imgOut)


        k = cv2.waitKey(20) & 0xFF  # stop on ESC
        if k == 27:
            break
    else:
        break

video.release()
cv2.destroyAllWindows()