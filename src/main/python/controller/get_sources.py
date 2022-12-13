import os


class GetResourcesFile(object):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_maps_x(cls, i):
        print(os.getcwd())
        return "../resources/base/data_config/maps/map_x_" + str(i) + ".npy"

    @classmethod
    def get_maps_y(cls, i):
        return "../resources/base/data_config/maps/map_y_" + str(i) + ".npy"

    @classmethod
    def get_matrix_perspective(cls, i):
        return "../resources/base/data_config/matrix/matrix_" + str(i) + ".npy"
