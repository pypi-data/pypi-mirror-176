import cv2

def under_sampling(arr, size=5):
    dst = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    img_size = dst.shape
    print("under gray", img_size)
    RATIO = img_size[0] / img_size[1]
    REAL_WIDTH = size*10
    REAL_HEIGHT = int(size*10 * RATIO)    

    dst = cv2.resize(dst, dsize=(REAL_WIDTH, REAL_HEIGHT), interpolation=cv2.INTER_AREA)
    return dst, (REAL_WIDTH, REAL_HEIGHT)


def under_sampling_color(arr, size=5):
    img_size = arr.shape
    RATIO = img_size[0] / img_size[1]
    REAL_WIDTH = size*10
    REAL_HEIGHT = int(size*10 * RATIO)    

    dst = cv2.resize(arr, dsize=(REAL_WIDTH, REAL_HEIGHT), interpolation=cv2.INTER_AREA)
    return dst, (REAL_WIDTH, REAL_HEIGHT)

