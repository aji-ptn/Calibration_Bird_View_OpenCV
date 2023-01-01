from PyQt6 import QtGui, QtCore, QtWidgets
import cv2


def select_directory(parent=None, title='Select Folder'):
    """
    Generate a dialog for directory selection and return the path of the directory
    selected. If no directory is selected, an empty string is returned.


    Returns:
        path of the directory selected

    - Example:

    .. code-block:: python

        path_dir = mutils.select_directory()
    """
    option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
    directory = QtWidgets.QFileDialog.getExistingDirectory(parent, title, options=option)
    return directory

def select_file(parent, title, dir_path, file_filter):
    """
    find file path from computer directory
    Args:
        parent:
        title:
        dir_path:
        file_filter:

    Returns:

    """
    option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, title, dir_path, file_filter, options=option)
    return file_path


def show_image_to_label(label, image, width, angle=0, plusIcon=False):
    """
    This function Display an image to the label widget on the user interface. It requires some arguments
    such as image, label name and image width. suppose you don't like to draw a center point icon (+)
    you can change the plusIcon argument to become False.

    Args:
        label: The label will contain image to show in your user interface
        image: Image that want to show on user interface
        width: the width of result image, this value will calculate the height following the ratio.
        angle: the angle of image
        plusIcon: Drawing the plus icon on the image, by default this will be False.
                    if you want to draw you have to change to be True.

    Returns:
        Showing image on the label

    - Example:

    .. code-block:: python

        image = MoilUtils.showImageToLabel(label, image, 400, 0, False)
    """

    height = calculate_height(image, width)
    image = resize_image(image, width)
    image = rotate_image(image, angle)
    if plusIcon:
        # draw plus icon on image and show to label
        h, w = image.shape[:2]
        w1 = round((w / 2) - 10)
        h1 = round(h / 2)
        w2 = round((w / 2) + 10)
        h2 = round(h / 2)
        w3 = round(w / 2)
        h3 = round((h / 2) - 10)
        w4 = round(w / 2)
        h4 = round((h / 2)) + 10
        cv2.line(image, (w1, h1), (w2, h2), (0, 255, 0), 1)
        cv2.line(image, (w3, h3), (w4, h4), (0, 255, 0), 1)

    label.setMinimumSize(QtCore.QSize(width, height))
    label.setMaximumSize(QtCore.QSize(width, height))
    image = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                         QtGui.QImage.Format.Format_RGB888).rgbSwapped()
    label.setPixmap(QtGui.QPixmap.fromImage(image))


def calculate_height(image, width):
    """
    Return the height value of an image by providing the width value. This high
    value is calculated by keeping the aspect ratio of the image.

    Args:
        image: original image
        width: size image we want

    Returns:
        height: height image

    - Example:

    .. code-block:: python

        height = calculate_height(image, 140)
    """

    h, w = image.shape[:2]
    r = width / float(w)
    height = round(h * r)
    return height


def rotate_image(src, angle, center=None, scale=1.0):
    """
    Rotation of images are among the most basic operations under the broader class of
    Affine transformations. This function will return the image after turning clockwise
    or anticlockwise depending on the angle given.

    Args:
        src: original image
        angle: the value angle for turn the image
        center: determine the specific coordinate to rotate image
        scale: scale image

    Returns:
        dst image: rotated image

    - Example:

    .. code-block:: python

        image = rotate_image(image, 90)
    """
    h, w = src.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    m = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(src, m, (w, h))
    return rotated


def resize_image(image, width):
    """
    Changing the dimensions of image according to the size width given (it use cv2.resize function from OpenCV).
    It will keep the aspect ratio of the original image.

    Args:
        image: image original
        width: image width we want

    Returns:
        result: image has been resize

    - Example:

    .. code-block:: python

        image = resize_image(image, 140)
    """
    h, w = image.shape[:2]
    r = width / float(w)
    hi = round(h * r)
    result = cv2.resize(image, (width, hi),
                        interpolation=cv2.INTER_AREA)
    return result


def init_ori_ratio(label, image):
    """
    Calculate the initial ratio of the image.

    Returns:
        ratio_x : ratio width between image and ui window.
        ratio_y : ratio height between image and ui window.
        center : find the center image on window user interface.
    """
    h = label.height()
    w = label.width()
    height, width = image.shape[:2]
    ratio_x = width / w
    ratio_y = height / h
    return ratio_x, ratio_y
