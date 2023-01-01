import datetime
import time

import numpy as np

from .additional_function import read_image
import cv2
from .merge_original_image import merge_original_image
from .model_video import ModelVideo
import yaml
from subprocess import call
from .gradient_class import create_blending
from .crop_gradient_center_config import crop_for_gradient_front_left, crop_for_gradient_front_right, \
    crop_for_gradient_rear_left, crop_for_gradient_rear_right, crop_region
from .model_data import MainData


class MainModel:
    def __init__(self):
        """
        This class is moin model for process all input base on the controller
        """
        super(MainModel, self).__init__()
        self.data_model = MainData()
        self.video_controller = ModelVideo(self)
        self.source_file = None
        self.data_model.data_config = None
        self.initial_properties()

    def set_source_file(self, source_file):
        """
        This function is for set source file in the image

        Args:
            source_file: source file

        Returns:

        """
        self.source_file = source_file

    def initial_properties(self):
        """
        This function is for initial image for the first time input image

        Returns:

        """
        if not self.data_model.data_config:
            self.data_model.properties_image = {}
        cam_total = 4
        self.data_model.calibration_image = {"matrix_k": [], "new_matrix_k": [], "dis_coefficient": [], "dimension": []}
        self.data_model.list_original_image = [None] * cam_total
        print(self.data_model.list_original_image)
        self.data_model.list_original_undistorted_image = [None] * cam_total
        self.data_model.list_undistorted_image = [None] * cam_total
        self.data_model.list_undistorted_drawing_image = [None] * cam_total
        self.data_model.list_perspective_image = [None] * cam_total
        self.data_model.list_perspective_drawing_image = [None] * cam_total

    def list_image_data(self, path_image, i):
        """
        This function is for read and create image list

        Args:
            path_image: image path
            i: index image

        Returns:

        """
        print(path_image)
        self.data_model.list_original_image[i] = read_image(path_image)
        self.process_original_undistorted(i)

    def list_intrinsic_data(self, path_parameter):
        """
        This function is for input list of parameter

        Args:
            path_parameter: location of parameter

        Returns:

        """
        K, D, dimension = self.read_parameter(path_parameter)
        print(K, D, list(dimension))

        self.data_model.calibration_image["matrix_k"].append(K)
        self.data_model.calibration_image["dis_coefficient"].append(D)
        self.data_model.calibration_image["dimension"].append(dimension)

    def update_union_original_image(self):
        """
        This function is for combine four image in to one image

        Returns:

        """
        self.data_model.union_original_image = merge_original_image(self.data_model.list_original_image)

    def update_intrinsic_parameter(self, i):
        """
        This function is for update intrinsic parameter

        Args:
            i: index file image

        Returns:

        """
        keys = list(self.data_model.properties_image)
        self.data_model.properties_image[keys[i]]["Ins"]["Fx"] = float(self.data_model.calibration_image["matrix_k"][i][0][0])
        self.data_model.properties_image[keys[i]]["Ins"]["Fy"] = float(self.data_model.calibration_image["matrix_k"][i][1][1])
        self.data_model.properties_image[keys[i]]["Ins"]["Icx"] = float(self.data_model.calibration_image["matrix_k"][i][0][2])
        self.data_model.properties_image[keys[i]]["Ins"]["Icy"] = float(self.data_model.calibration_image["matrix_k"][i][1][2])
        self.data_model.properties_image[keys[i]]["Ins"]["Width"] = int(self.data_model.calibration_image["dimension"][i][0])
        self.data_model.properties_image[keys[i]]["Ins"]["Height"] = int(self.data_model.calibration_image["dimension"][i][1])

    def process_undistorted_image(self, i):
        """
        this function is for process undistortion image

        Args:
            i: index of image

        Returns:

        """
        keys = list(self.data_model.properties_image)
        new_matrix = self.data_model.calibration_image["matrix_k"][i].copy()
        new_matrix[0, 0] = self.data_model.properties_image[keys[i]]["Ins"]["Fx"]
        new_matrix[1, 1] = self.data_model.properties_image[keys[i]]["Ins"]["Fy"]
        new_matrix[0, 2] = self.data_model.properties_image[keys[i]]["Ins"]["Icx"]
        new_matrix[1, 2] = self.data_model.properties_image[keys[i]]["Ins"]["Icy"]

        print(new_matrix)

        self.data_model.calibration_image["new_matrix_k"] = new_matrix

        width = self.data_model.properties_image[keys[i]]["Ins"]["Width"]
        height = self.data_model.properties_image[keys[i]]["Ins"]["Height"]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.data_model.calibration_image["matrix_k"][i],
                                                         self.data_model.calibration_image["dis_coefficient"][i], np.eye(3),
                                                         self.data_model.calibration_image["new_matrix_k"],
                                                         (width, height), cv2.CV_16SC2)

        path_map_x_anypoint = self.source_file.get_maps_x(i)
        path_map_y_anypoint = self.source_file.get_maps_y(i)

        np.save(path_map_x_anypoint, map1)
        np.save(path_map_y_anypoint, map2)

        undistorted = cv2.remap(self.data_model.list_original_image[i], map1, map2,
                                interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        self.data_model.list_undistorted_image[i] = undistorted
        self.draw_point_position("src", keys, i)

    def process_original_undistorted(self, i):
        """
        This function uis for process undistortion image using initial parameter

        Args:
            i: index of image

        Returns:

        """
        width, height = self.data_model.calibration_image["dimension"][i]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.data_model.calibration_image["matrix_k"][i],
                                                         self.data_model.calibration_image["dis_coefficient"][i], np.eye(3),
                                                         self.data_model.calibration_image["matrix_k"][i],
                                                         (int(width), int(height)),
                                                         cv2.CV_16SC2)
        self.data_model.list_original_undistorted_image[i] = cv2.remap(self.data_model.list_original_image[i], map1, map2,
                                                                  interpolation=cv2.INTER_LINEAR,
                                                                  borderMode=cv2.BORDER_CONSTANT)

    def load_config(self, config_file):
        """
        This function is for load data from directory

        Args:
            config_file: config file directory

        Returns:

        """
        with open(config_file, "r") as file:
            data = yaml.safe_load(file)
        self.data_model.data_config = True
        self.data_model.properties_image = data

    def save_config_to_file(self, directory_path):
        """
        This function is for save image into directory file

        Args:
            data: data properties

        Returns:

        """
        print("save")
        properties_image = self.data_model.properties_image
        with open(directory_path + "/data", "w") as outfile:
            yaml.dump(properties_image, outfile, default_flow_style=False)

    def process_perspective_image(self, i):
        """
        This function is for crete perspective ground image
        Args:
            i: index of image

        Returns:

        """
        # start = time.time()
        keys = list(self.data_model.properties_image)
        canvas = self.data_model.properties_image[keys[i]]["dst"]["Width"], self.data_model.properties_image[keys[i]]["dst"][
            "Height"]
        src = np.float32(
            [[self.data_model.properties_image[keys[i]]["src"]["point1_x"],
              self.data_model.properties_image[keys[i]]["src"]["point1_y"]],
             [self.data_model.properties_image[keys[i]]["src"]["point2_x"],
              self.data_model.properties_image[keys[i]]["src"]["point2_y"]],
             [self.data_model.properties_image[keys[i]]["src"]["point3_x"],
              self.data_model.properties_image[keys[i]]["src"]["point3_y"]],
             [self.data_model.properties_image[keys[i]]["src"]["point4_x"],
              self.data_model.properties_image[keys[i]]["src"]["point4_y"]]])
        dst = np.float32(
            [[self.data_model.properties_image[keys[i]]["dst"]["point1_x"],
              self.data_model.properties_image[keys[i]]["dst"]["point1_y"]],
             [self.data_model.properties_image[keys[i]]["dst"]["point2_x"],
              self.data_model.properties_image[keys[i]]["dst"]["point2_y"]],
             [self.data_model.properties_image[keys[i]]["dst"]["point3_x"],
              self.data_model.properties_image[keys[i]]["dst"]["point3_y"]],
             [self.data_model.properties_image[keys[i]]["dst"]["point4_x"],
              self.data_model.properties_image[keys[i]]["dst"]["point4_y"]]])

        matrix = cv2.getPerspectiveTransform(src, dst)
        # self.data_model.properties_image[keys[i]]["matrix"] = matrix
        # self.data_model.list_perspective_image[i] = cv2.warpPerspective(self.data_model.list_undistorted_image[i],
        #                                                            self.data_model.properties_image[keys[i]]["matrix"],
        #                                                            canvas)
        self.data_model.list_perspective_image[i] = cv2.warpPerspective(self.data_model.list_undistorted_image[i],
                                                                   matrix,
                                                                   canvas)

        path_matrix = self.source_file.get_matrix_perspective(i)

        np.save(path_matrix, matrix)

        print("----------------")
        # print(time.time() - start)
        print("----------------")
        # print(self.data_model.properties_image[keys[i]]["matrix"])

        self.draw_point_position("dst", keys, i)

    def draw_point_position(self, position, keys, i):
        """
        This function is foe draw four point dst or src in image

        Args:
            position: location of point in pixel
            keys: name of image
            i: index of image

        Returns:

        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        if position == "dst":
            self.data_model.list_perspective_drawing_image[i] = self.data_model.list_perspective_image[i].copy()
            image = self.data_model.list_perspective_drawing_image[i]
            font_color = (77, 180, 215)
        elif position == "src":
            self.data_model.list_undistorted_drawing_image[i] = self.data_model.list_undistorted_image[i].copy()
            image = self.data_model.list_undistorted_drawing_image[i]
            font_color = (72, 191, 145)
        else:
            image = None
            font_color = None
        cv2.circle(image, (self.data_model.properties_image[keys[i]][position]["point1_x"],
                           self.data_model.properties_image[keys[i]][position]["point1_y"]), 20, (200, 0, 0), 5)
        # cv2.putText(image, '1', (self.data_model.properties_image[keys[i]][position]["point1_x"],
        #                          self.data_model.properties_image[keys[i]][position]["point1_y"]), font,
        #             5, font_color, 5, cv2.LINE_AA)
        cv2.circle(image, (self.data_model.properties_image[keys[i]][position]["point2_x"],
                           self.data_model.properties_image[keys[i]][position]["point2_y"]), 20, (0, 200, 0), 5)
        # cv2.putText(image, '2', (self.data_model.properties_image[keys[i]][position]["point2_x"],
        #                          self.data_model.properties_image[keys[i]][position]["point2_y"]), font,
        #             5, font_color, 5, cv2.LINE_AA)
        cv2.circle(image, (self.data_model.properties_image[keys[i]][position]["point3_x"],
                           self.data_model.properties_image[keys[i]][position]["point3_y"]), 20, (0, 200, 255), 5)
        # cv2.putText(image, '3', (self.data_model.properties_image[keys[i]][position]["point3_x"],
        #                          self.data_model.properties_image[keys[i]][position]["point3_y"]), font,
        #             5, font_color, 5, cv2.LINE_AA)
        cv2.circle(image, (self.data_model.properties_image[keys[i]][position]["point4_x"],
                           self.data_model.properties_image[keys[i]][position]["point4_y"]), 20, (200, 0, 255), 5)
        # cv2.putText(image, '4', (self.data_model.properties_image[keys[i]][position]["point4_x"],
        #                          self.data_model.properties_image[keys[i]][position]["point4_y"]), font,
        #             5, font_color, 5, cv2.LINE_AA)
        if position == "dst":
            self.data_model.list_perspective_drawing_image[i] = image
        elif position == "src":
            self.data_model.list_undistorted_drawing_image[i] = image

    @classmethod
    def read_parameter(cls, path_parameter):
        """
        This function is for read parameter from input data

        Args:
            path_parameter: path of parameter

        Returns:

        """
        file = cv2.FileStorage(path_parameter, cv2.FILE_STORAGE_READ)
        camera_matrix = file.getNode("camera_matrix").mat()
        dist_coefficient = file.getNode("dist_coeffs").mat()
        resolution = file.getNode("resolution").mat().flatten()
        file.release()
        K = np.array(camera_matrix)
        D = np.array(dist_coefficient)
        dimension = np.array(resolution)

        return K, D, dimension

    def update_overlap_or_bird_view(self):
        """
        This function is for update image overlap or bird view

        Returns:

        """
        try:
            self.data_model.overlap_image = self.process_bird_view("image")
            if self.data_model.properties_video["video"]:
                self.data_model.bird_view_video = self.process_bird_view("video")
        except:
            pass

    def update_bird_view_video(self):
        """
            This function is for update image
        Returns:

        """
        self.data_model.bird_view_video = self.process_bird_view("video")

    def process_bird_view(self, image_sources):
        """
        This function is for process bird view image

        Args:
            image_sources: image source mode, (perspective ground view)

        Returns:

        """
        if image_sources == "image":
            image = self.data_model.list_perspective_image
            activation = self.data_model.gradient_image
        else:
            image = self.data_model.list_perspective_video
            activation = self.data_model.properties_video["mode"]
        # print("Bird view")
        image = [image[0],
                 cv2.rotate(image[1], cv2.ROTATE_90_COUNTERCLOCKWISE),
                 cv2.rotate(image[2], cv2.ROTATE_90_CLOCKWISE),
                 cv2.rotate(image[3], cv2.ROTATE_180)]

        if image[3].shape[1] == image[0].shape[1] and image[2].shape[0] == image[1].shape[0]:
            canvas_bird_view = np.zeros([image[1].shape[0], image[0].shape[1], 3], dtype=np.uint8)
            right_limit = canvas_bird_view.shape[1] - image[2].shape[1]
            rear_limit = canvas_bird_view.shape[0] - image[3].shape[0]

            # image[0] = self.remove_black(image[0])
            # image[1] = self.remove_black(image[1])
            # image[2] = self.remove_black(image[2])
            # image[3] = self.remove_black(image[3])

            canvas_bird_view[0:0 + image[1].shape[0], 0:0 + image[1].shape[1]] = image[1]
            canvas_bird_view[0:0 + image[2].shape[0], right_limit:right_limit + image[2].shape[1]] = image[2]
            canvas_bird_view[0:0 + image[0].shape[0], 0:0 + image[0].shape[1]] = image[0]
            canvas_bird_view[rear_limit:rear_limit + image[3].shape[0], 0:0 + image[3].shape[1]] = image[3]
            # self.data_model.overlap_image = canvas_bird_view

            if activation == "bird_view":
                canvas_bird_view = self.bird_view_combine_overlapping(image)
                canvas_bird_view = cv2.cvtColor(canvas_bird_view, cv2.COLOR_BGRA2BGR)

            else:
                list_overlapping, pos_fr_le_x, pos_fr_le_y, pos_fr_ri_y, pos_rea_le_x \
                    = self.find_overlap_gradient(image, right_limit, rear_limit, activation)

                canvas_bird_view[pos_fr_le_y:pos_fr_le_y + list_overlapping[0].shape[0],
                pos_fr_le_x:pos_fr_le_x + list_overlapping[0].shape[1]] = list_overlapping[0]  # front left

                canvas_bird_view[rear_limit:rear_limit + list_overlapping[2].shape[0],
                pos_rea_le_x:pos_rea_le_x + list_overlapping[2].shape[1]] = list_overlapping[2]  # left rear

                canvas_bird_view[pos_fr_ri_y:pos_fr_ri_y + list_overlapping[1].shape[0],
                right_limit:right_limit + list_overlapping[1].shape[1]] = list_overlapping[1]  # front right

                canvas_bird_view[rear_limit:rear_limit + list_overlapping[3].shape[0],
                image[3].shape[1] - image[2].shape[1]: image[3].shape[1] - image[2].shape[1] +
                                                       list_overlapping[3].shape[1]] = list_overlapping[3]  # right rear

            return canvas_bird_view

    @classmethod
    def transfer(cls, src):
        # src = cv2.resize(src, (int(src.shape[1]/2), int(src.shape[0]/2)))
        tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(src)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)
        return dst

    def bird_view_combine_overlapping(self, image):
        """
        This function is for combine image in to bird view

        Args:
            image: image perspective ground view

        Returns:

        """
        for i in range(len(image)):
            image[i] = self.transfer(image[i])

        final_image_front = np.zeros([image[1].shape[0], image[0].shape[1], 4], dtype=np.uint8)
        final_image_left = np.zeros([image[1].shape[0], image[0].shape[1], 4], dtype=np.uint8)
        final_image_right = np.zeros([image[1].shape[0], image[0].shape[1], 4], dtype=np.uint8)
        final_image_rear = np.zeros([image[1].shape[0], image[0].shape[1], 4], dtype=np.uint8)

        right_limit = final_image_right.shape[1] - image[2].shape[1]
        rear_limit = final_image_rear.shape[0] - image[3].shape[0]

        final_image_left[0:0 + image[1].shape[0], 0:0 + image[1].shape[1]] = image[1]
        final_image_right[0:0 + image[2].shape[0], right_limit:right_limit + image[2].shape[1]] = image[2]
        final_image_front[0:0 + image[0].shape[0], 0:0 + image[0].shape[1]] = image[0]
        final_image_rear[rear_limit:rear_limit + image[3].shape[0], 0:0 + image[3].shape[1]] = image[3]

        res = final_image_left[:]
        cnd = final_image_right[:, :, 3] > 0
        res[cnd] = final_image_right[cnd]
        cnd = final_image_front[:, :, 3] > 0
        res[cnd] = final_image_front[cnd]
        cnd = final_image_rear[:, :, 3] > 0
        res[cnd] = final_image_rear[cnd]

        return res

    @classmethod
    def find_overlap_gradient(cls, image, right_limit, rear_limit, gradient_mode):
        """
        This function is for create overlap between image

        Args:
            image: perspective ground view image
            right_limit: additional value for position right image
            rear_limit: additional value for position rear image
            gradient_mode: mode of gradien image

        Returns:

        """
        image_overlap = [None] * len(image)
        crop_front_left = image[0][0:image[0].shape[0], 0:image[1].shape[1]]
        crop_left_front = image[1][0:image[0].shape[0], 0:image[1].shape[1]]

        crop_front_right = image[0][0:image[0].shape[0], right_limit:right_limit + image[2].shape[1]]
        crop_right_front = image[2][0:image[0].shape[0], 0:image[2].shape[1]]

        crop_left_rear = image[1][rear_limit:rear_limit + image[3].shape[0], 0:image[1].shape[1]]
        crop_rear_left = image[3][0:image[3].shape[0], 0:image[1].shape[1]]

        crop_right_rear = image[2][rear_limit:rear_limit + image[3].shape[0], 0:image[2].shape[1]]
        crop_rear_right = image[3][0:image[3].shape[0], image[3].shape[1] - image[2].shape[1]:
                                                        image[3].shape[1] - image[2].shape[1] + image[3].shape[1]]
        pos_fr_le_x, pos_fr_le_y, pos_fr_ri_y, pos_rea_le_x = 0, 0, 0, 0
        if gradient_mode == "O":
            image_overlap[0] = cv2.addWeighted(crop_front_left, 0.5, crop_left_front, 0.5, 0)  # overlap_front_left
            image_overlap[1] = cv2.addWeighted(crop_front_right, 0.5, crop_right_front, 0.5, 0)  # overlap_front_right
            image_overlap[2] = cv2.addWeighted(crop_left_rear, 0.5, crop_rear_left, 0.5, 0)  # overlap_left_rear
            image_overlap[3] = cv2.addWeighted(crop_right_rear, 0.5, crop_rear_right, 0.5, 0)  # overlap_right_rear

        else:
            if gradient_mode == "D":  # front left  --------------------------------------------------------------------
                pos_fr_le_x, pos_fr_le_y, crop_front_left, crop_left_front = crop_for_gradient_front_left(
                    crop_front_left,
                    crop_left_front)

            front_left_ov = crop_region(crop_front_left, "front_left", gradient_mode)
            left_front_ov = crop_region(crop_left_front, "left_front", gradient_mode)
            try:
                image_overlap[0] = create_blending(front_left_ov, left_front_ov)
            except:
                image_overlap[0] = cv2.addWeighted(crop_front_left, 0.5, crop_left_front, 0.5, 0)  # overlap_front_left

            if gradient_mode == "D":  # front right  -------------------------------------------------------------------
                _, pos_fr_ri_y, crop_front_right, crop_right_front = crop_for_gradient_front_right(crop_front_right,
                                                                                                   crop_right_front)
            front_right_ov = crop_region(crop_front_right, "front_right", gradient_mode)
            right_front_ov = crop_region(crop_right_front, "right_front", gradient_mode)
            try:
                image_overlap[1] = create_blending(front_right_ov, right_front_ov)
            except:
                image_overlap[1] = cv2.addWeighted(crop_front_right, 0.5, crop_right_front, 0.5,
                                                   0)  # overlap_front_right

            if gradient_mode == "D":  # rear left  ---------------------------------------------------------------------
                pos_rea_le_x, _, crop_left_rear, crop_rear_left = crop_for_gradient_rear_left(crop_left_rear,
                                                                                              crop_rear_left)

            image_overlap[2] = cv2.addWeighted(crop_left_rear, 0.5, crop_rear_left, 0.5, 0)  # overlap_left_rear

            left_rear_ov = crop_region(crop_left_rear, "left_rear", gradient_mode)
            rear_left_ov = crop_region(crop_rear_left, "rear_left", gradient_mode)
            try:
                image_overlap[2] = create_blending(left_rear_ov, rear_left_ov)
            except:
                image_overlap[2] = cv2.addWeighted(crop_left_rear, 0.5, crop_rear_left, 0.5, 0)  # overlap_left_rear

            if gradient_mode == "D":  # rear right ---------------------------------------------------------------------
                _, _, crop_right_rear, crop_rear_right = crop_for_gradient_rear_right(crop_right_rear, crop_rear_right)
            right_rear_ov = crop_region(crop_right_rear, "right_rear", gradient_mode)
            rear_right_ov = crop_region(crop_rear_right, "rear_right", gradient_mode)
            try:
                image_overlap[3] = create_blending(right_rear_ov, rear_right_ov)
            except:
                image_overlap[3] = cv2.addWeighted(crop_right_rear, 0.5, crop_rear_right, 0.5, 0)  # overlap_right_rear

        return image_overlap, pos_fr_le_x, pos_fr_le_y, pos_fr_ri_y, pos_rea_le_x

    def crop_image(self, image, x, y):
        """
        crop image

        Args:
            image: image perspective ground view
            x: x axis value
            y: y axis value

        Returns:

        """
        img = cv2.circle(image.copy(), (x, y), 2, (200, 5, 200), -1)
        img = img[y - 70: (y - 70) + 140, x - 70:(x - 70) + 140]
        # cv2.imwrite("img.jpg", img)
        return img

    def get_data_position(self, i_image, data):
        """
        This function is for load data position in to the parameter
        Args:
            i_image: index image
            data: data image

        Returns:

        """
        keys = list(self.data_model.properties_image)
        self.data_model.properties_image[keys[i_image]]["src"]["point1_x"] = data[0][0]
        self.data_model.properties_image[keys[i_image]]["src"]["point1_y"] = data[0][1]
        self.data_model.properties_image[keys[i_image]]["src"]["point2_x"] = data[1][0]
        self.data_model.properties_image[keys[i_image]]["src"]["point2_y"] = data[1][1]
        self.data_model.properties_image[keys[i_image]]["src"]["point3_x"] = data[2][0]
        self.data_model.properties_image[keys[i_image]]["src"]["point3_y"] = data[2][1]
        self.data_model.properties_image[keys[i_image]]["src"]["point4_x"] = data[3][0]
        self.data_model.properties_image[keys[i_image]]["src"]["point4_y"] = data[3][1]
        # print(self.data_model.properties_image[keys[i_image]]["src"])

    def load_config_authentication(self, data_config):
        """
        This function is for load data authentication

        Args:
            data_config: config data login

        Returns:

        """
        with open(data_config, "r") as file:
            data = yaml.safe_load(file)

        self.authen = data

    def authentication(self, password_in=None):
        """

        Args:
            password_in:

        Returns:

        """
        if password_in is not None:
            self.authen["data"] = password_in
            password = password_in
        else:
            password = self.authen["data"]

        # result = os.system("echo '{}' | sudo -Si".format(str(password.strip())))  # important: strip() the newline char
        cmd = 'chmod -R 777 /opt/MoilDash'
        result = call('echo {} | sudo -S {}'.format(password, cmd), shell=True)

        if result == "0" or result == 0:
            status = True
        else:
            status = False
        return status

    def save_config_authentication(self, d_password, file):
        # encMessage = self.encrypting_data(d_password)
        # self.data = encMessage
        self.authen["data"] = d_password
        # file = self..app_ctxt.get_resource("data/data.yaml")
        with open(file, "w") as outfile:
            yaml.dump(self.authen, outfile, default_flow_style=False)
            print("save config success")

    def save_image(self, directory_path):
        """
        This function is for save image to the directory
        Returns:

        """
        if self.data_model.overlap_image is not None:
            x = datetime.datetime.now()
            print("saved")
            time = x.strftime("%Y_%m_%d_%H_%M_%S")
            cv2.imwrite(directory_path + "/overlap_" + time + ".jpg", self.data_model.overlap_image)

            # i = 0
            # for undis, pers, pers2 in zip(self.data_model.list_undistorted_drawing_image,
            #                               self.data_model.list_perspective_drawing_image,
            #                               self.data_model.list_perspective_image):
            #     cv2.imwrite(directory_path + "/undis_point" + str(i) + ".jpg", undis)
            #     cv2.imwrite(directory_path + "/pers_point" + str(i) + ".jpg", pers)
            #     cv2.imwrite(directory_path + "/pers" + str(i) + ".jpg", pers2)
            #     i += 1

    def change_mode_gradient_image(self, mode):
        """
        This function is for change mode gradient
        Args:
            mode:

        Returns:

        """
        self.data_model.gradient_image = mode
        self.data_model.overlap_image = self.process_bird_view("image")
