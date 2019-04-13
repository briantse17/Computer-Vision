import cv2
import numpy as np
import queue
from threading import Thread

drawing = False  # true if mouse is pressed
fill = False  # if True, left click inside of shape will trigger fill function

img = cv2.imread('test2.jpg')
height, width, channel = img.shape
mask_img = np.zeros((height, width, channel), dtype=np.uint8)

def interactive_drawing(event, x, y, flags, param):
    """ mouse callback function """
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN and fill == False:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONDOWN and fill == True:
        Thread(target = floodfill, args = (mask_img, (x, y), )).start()

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.line(mask_img, (ix, iy), (x, y), [255, 255, 255], 5)
            ix = x
            iy = y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if fill == False:
            cv2.line(mask_img, (ix, iy), (x, y), [255, 255, 255], 5)


def floodfill(img, pos):
    """ flood fill region """

    q = queue.Queue()
    q.put(pos)

    IsBounded = True
    bbox = np.where(img == 255)
    if not bbox:
        return

    bbox = np.min(bbox[1]), np.max(bbox[1]), np.min(bbox[0]), np.max(bbox[0])
    while not q.empty():
        x, y = q.get()
        if x < bbox[0] or x >= bbox[1] or y < bbox[2] or y >= bbox[3]:
            IsBounded = False
            break

        if np.any(img[y][x] == 255):
            continue

        img[y][x] = 255
        q.put((x + 1, y))
        q.put((x - 1, y))
        q.put((x, y + 1))
        q.put((x, y - 1))

    # check if circle was complete
    if not IsBounded:
        img[:, :] = 0
        return

cv2.namedWindow('Window')
cv2.setMouseCallback('Window', interactive_drawing)
while True:
    cv2.imshow('Window', np.bitwise_or(img, mask_img))
    k = cv2.waitKey(1) & 0xFF
    if k == ord('f'):
        fill = True
    elif k == ord('d'):
        fill = False
    elif k == ord('q'):
        break
    elif k == ord('r'):
        mask_img[:, :] = 0
    elif k == ord('s'):
        cv2.imshow('Mask', mask_img)
        cv2.imwrite("/Users/btse/Desktop/Result.png", mask_img)

cv2.destroyAllWindows()