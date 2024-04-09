import cv2 as cv

print(cv.__version__)


def blur(img):
    """Гауссово размытие"""
    h, w = img.shape[:2]

    # нечетные коэффициенты размытия
    dw, dh = int(w / 3), int(h / 3)
    if dw % 2 == 0: dw -= 1
    if dh % 2 == 0: dh -= 1

    sigma = 0
    return cv.GaussianBlur(img, (dw, dh), sigma)


capture = cv.VideoCapture(0)  # 0 = дефолтная камера
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, img = capture.read()

    # определение массива с несколькими лицами
    faces = face_cascade.detectMultiScale(img,
                                          scaleFactor=1.2,  # слегка увеличит прямоугольник
                                          minNeighbors=5,  # аналог точности
                                          minSize=(20, 20)  # минимальный размер
                                          )

    for x, y, w, h in faces:
        cv.rectangle(img,
                     (x, y), (x + w, y + h),
                     (255, 0, 0),  # цвет BGR (не RGB!)
                     2  # толщина границ
                     )
        img[y:y + h, x:x + w] = blur(img[y:y + h, x:x + w])  # замена куска картинки на заданную матрицу

    cv.imshow('Main Camera', img)

    key = cv.waitKey(30) & 0xFF  # 'esc'
    if key == 27: break

capture.release()  # забыть камеру
cv.destroyAllWindows()  # уничтожить все созданные cv2 окна
