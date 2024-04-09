import cv2 as cv

img = cv.imread('colored_lion.jpg')
b = g = r = 0
clicked = False


def color_fn(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONUP:
        global b, g, r, clicked
        b, g, r = img[y, x]  # координаты перевернуты!
        clicked = True


cv.namedWindow('main')
cv.setMouseCallback('main', color_fn)  # события мыши

while True:
    cv.imshow('main', img)

    if clicked:
        print((b, g, r))
        cv.rectangle(img, (50, 50), (300, 100), (int(b), int(g), int(r)), -1)
        cv.putText(img, f'R{r}G{g}B{b}', (50, 100), 2, 1.0, (255, 255, 255))
        clicked = False

    if cv.waitKey(20) & 0xFF == 27:
        break

cv.destroyAllWindows()
