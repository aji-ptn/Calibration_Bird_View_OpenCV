import numpy as np


def merge_original_image(image_ori):
    """
    This function will combine images
    Args:
        image_ori: list of original image

    Returns:

    """
    if image_ori[0] is not None and image_ori[1] is None:
        height = image_ori[0].shape[0]
        width = image_ori[0].shape[1]
        merge_image_canvas = np.zeros([height, width, 3], dtype=np.uint8)
        merge_image_canvas.fill(255)
        merge_image_canvas[0:image_ori[0].shape[0],
        0:0 + image_ori[0].shape[1]] = image_ori[0]

    elif image_ori[1] is not None and image_ori[2] is None:
        height = image_ori[0].shape[0]
        width = image_ori[0].shape[1] + image_ori[1].shape[1] + 50
        merge_image_canvas = np.zeros([height, width, 3], dtype=np.uint8)
        merge_image_canvas.fill(255)

        merge_image_canvas[0:image_ori[0].shape[0],
        0:0 + image_ori[0].shape[1]] = image_ori[0]

        pos_x_1 = image_ori[0].shape[1] + 50
        pos_y_1 = 0
        merge_image_canvas[pos_y_1:pos_y_1 + image_ori[1].shape[0],
        pos_x_1:pos_x_1 + image_ori[1].shape[1]] = image_ori[1]

    elif image_ori[2] is not None and image_ori[3] is None:
        height = image_ori[0].shape[0] + image_ori[2].shape[0] + 50
        width = image_ori[0].shape[1] + image_ori[1].shape[1] + 50
        merge_image_canvas = np.zeros([height, width, 3], dtype=np.uint8)
        merge_image_canvas.fill(255)
        merge_image_canvas[0:image_ori[0].shape[0],
        0:0 + image_ori[0].shape[1]] = image_ori[0]

        pos_x_1 = image_ori[0].shape[1] + 50
        pos_y_1 = 0
        merge_image_canvas[pos_y_1:pos_y_1 + image_ori[1].shape[0],
        pos_x_1:pos_x_1 + image_ori[1].shape[1]] = image_ori[1]

        pos_x_2 = 0
        pos_y_2 = image_ori[0].shape[0] + 50
        merge_image_canvas[pos_y_2:pos_y_2 + image_ori[1].shape[0],
        pos_x_2:pos_x_2 + image_ori[1].shape[1]] = image_ori[2]

    elif image_ori[3] is not None == 4:
        height = image_ori[0].shape[0] + image_ori[2].shape[0] + 50
        width = image_ori[0].shape[1] + image_ori[1].shape[1] + 50
        merge_image_canvas = np.zeros([height, width, 3], dtype=np.uint8)
        merge_image_canvas.fill(255)
        merge_image_canvas[0:image_ori[0].shape[0],
        0:0 + image_ori[0].shape[1]] = image_ori[0]

        pos_x_1 = image_ori[0].shape[1] + 50
        pos_y_1 = 0
        merge_image_canvas[pos_y_1:pos_y_1 + image_ori[1].shape[0],
        pos_x_1:pos_x_1 + image_ori[1].shape[1]] = image_ori[1]

        pos_x_2 = 0
        pos_y_2 = image_ori[0].shape[0] + 50
        merge_image_canvas[pos_y_2:pos_y_2 + image_ori[1].shape[0],
        pos_x_2:pos_x_2 + image_ori[2].shape[1]] = image_ori[2]

        pos_x_3 = image_ori[0].shape[1] + 50
        pos_y_3 = image_ori[0].shape[0] + 50
        merge_image_canvas[pos_y_3:pos_y_3 + image_ori[1].shape[0],
        pos_x_3:pos_x_3 + image_ori[3].shape[1]] = image_ori[3]

    else:
        merge_image_canvas = None

    return merge_image_canvas