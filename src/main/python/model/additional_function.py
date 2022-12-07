import cv2


def read_image(path_image):
    image = cv2.imread(path_image)
    if image is None:
        raise FileNotFoundError("`{}` cannot be loaded".format(path_image))
    return image
