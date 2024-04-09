# pip install nomeroff-net

import cv2 as cv
import imutils

image = cv.imread('plates/plate (1).jpg')
height, width, color_profile = image.shape
cv.imshow('image', image)
cv.waitKey()  # ожидать нажатие клавиши для закрытия картинки

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # не RGB а BGR - привет американцы-выпендрежи
cv.imshow('gray', gray)
cv.waitKey()  # ожидать нажатие клавиши для закрытия картинки

# выделение участков на thresh тонов темнее
black = cv.threshold(gray, 0,
                     255,  # максимальное значение альфа = яркость
                     cv.THRESH_OTSU)[1]
cv.imshow('black', black)
cv.waitKey()  # ожидать нажатие клавиши для закрытия картинки

# выделение контуров
edges = cv.Canny(gray,
                 10,  # маленькие контуры
                 250,  # большие контуры
                 )
cv.imshow('edges', edges)
cv.waitKey()  # ожидать нажатие клавиши для закрытия картинки

# закрытие шумных контуров
kernel = cv.getStructuringElement(cv.MORPH_RECT,
                                  (7, 7)  # размер печатки (кисти)
                                  )
closed = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)
cv.imshow('closed', closed)
cv.waitKey()  # ожидать нажатие клавиши для закрытия картинки

# поиск контуров
cntrs = cv.findContours(closed.copy(),
                        cv.RETR_EXTERNAL,  # алгоритм поиска контуров
                        cv.CHAIN_APPROX_SIMPLE,  # аппроксимация
                        )
cntrs = imutils.grab_contours(cntrs)

k = 0

# сглаживание контура
for c in cntrs:
    # длина контура
    p = cv.arcLength(c,
                     True,  # замкнутость контура
                     )
    # количество вершин контура
    approx = cv.approxPolyDP(c,
                             0.02 * p,  # сглаживание контура путем уменьшения его длины
                             True,  # замкнутость контура
                             )
    if len(approx) == 4:
        cv.drawContours(image,
                        [approx],  # сами контуры в виде вершин
                        -1,  # индекс контура -1 = нас не интересует
                        (0, 255, 0),  # цвет контура
                        4,  # толщина контура
                        )
        k += 1

print(k)
cv.imshow('plate', image)
cv.waitKey()  # ожидать нажатие клавиши для закрытия картинки

exit()

# выделение контура знака
cntrs = cv.findContours(black,
                        cv.RETR_TREE,  # алгоритм поиска контура как проход по древу
                        cv.CHAIN_APPROX_SIMPLE,  # аппроксимация
                        )
cntrs, _ = contours.sort_contours(cntrs[0])  # выбираем [0] контур

for cntr in cntrs:
    area = cv.contourArea(cntr)
    x, y, w, h = cv.boundingRect(cntr)
    if area > 5000:
        img = image[y:y + h, x:x + w]
