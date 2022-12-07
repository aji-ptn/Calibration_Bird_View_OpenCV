class MainData:
    def __init__(self):
        super(MainData, self).__init__()

        # data
        self.__total_camera_used = 4
        self.__camera_placement = None
        self.__gradient_image = "O"
        self.__properties_image = {}
        self.__calibration_image = {"matrix_k": [], "new_matrix_k": [], "dis_coefficient": [], "dimension": []}
        self.__data_config = None

        # image
        self.__list_original_image = []
        self.__list_undistorted_image = []
        self.__list_undistorted_drawing_image = []
        self.__list_original_undistorted_image = []
        self.__list_perspective_image = []
        self.__list_perspective_drawing_image = []
        self.__union_original_image = None
        self.__overlap_image = None
        self.__bird_view_image = None

        # video
        self.__list_frame_video = []
        self.__list_frame_undistorted_video = []
        self.__list_perspective_video = []
        self.__list_union_original_video = []
        self.__bird_view_video = None
        self.__properties_video = {"video": False, "streaming": False, "mode": "O", "pos_frame": 0, "frame_count": 0,
                                   "total_minute": 0, "total_second": 0, "current_minute": 0, "current_second": 0}

    # ===================================== data=====================================
    @property
    def total_camera_used(self):
        return self.__total_camera_used

    @total_camera_used.setter
    def total_camera_used(self, value):
        self.__total_camera_used = value

    @property
    def camera_placement(self):
        return self.__camera_placement

    @camera_placement.setter
    def camera_placement(self, value):
        self.__camera_placement = value

    @property
    def gradient_image(self):
        return self.__gradient_image

    @gradient_image.setter
    def gradient_image(self, value):
        self.__gradient_image = value

    @property
    def properties_image(self):
        return self.__properties_image

    @properties_image.setter
    def properties_image(self, value):
        self.__properties_image = value

    @property
    def data_config(self):
        return self.__data_config

    @data_config.setter
    def data_config(self, value):
        self.__data_config = value

    @property
    def calibration_image(self):
        return self.__calibration_image

    @calibration_image.setter
    def calibration_image(self, value):
        self.__calibration_image = value

    # ===================================== image =====================================
    @property
    def list_original_image(self):
        return self.__list_original_image

    @list_original_image.setter
    def list_original_image(self, value):
        self.__list_original_image = value

    @property
    def list_undistorted_image(self):
        return self.__list_undistorted_image

    @list_undistorted_image.setter
    def list_undistorted_image(self, value):
        self.__list_undistorted_image = value

    @property
    def list_undistorted_drawing_image(self):
        return self.__list_undistorted_drawing_image

    @list_undistorted_drawing_image.setter
    def list_undistorted_drawing_image(self, value):
        self.__list_undistorted_drawing_image = value

    @property
    def list_original_undistorted_image(self):
        return self.__list_original_undistorted_image

    @list_original_undistorted_image.setter
    def list_original_undistorted_image(self, value):
        self.__list_original_undistorted_image = value

    @property
    def list_perspective_image(self):
        return self.__list_perspective_image

    @list_perspective_image.setter
    def list_perspective_image(self, value):
        self.__list_perspective_image = value

    @property
    def list_perspective_drawing_image(self):
        return self.__list_perspective_drawing_image

    @list_perspective_drawing_image.setter
    def list_perspective_drawing_image(self, value):
        self.__list_perspective_drawing_image = value

    @property
    def union_original_image(self):
        return self.__union_original_image

    @union_original_image.setter
    def union_original_image(self, value):
        self.__union_original_image = value

    @property
    def overlap_image(self):
        return self.__overlap_image

    @overlap_image.setter
    def overlap_image(self, value):
        self.__overlap_image = value

    @property
    def bird_view_image(self):
        return self.__bird_view_image

    @bird_view_image.setter
    def bird_view_image(self, value):
        self.__bird_view_image = value

    # ===================================== video =====================================
    @property
    def list_frame_video(self):
        return self.__list_frame_video

    @list_frame_video.setter
    def list_frame_video(self, value):
        self.__list_frame_video = value

    @property
    def list_frame_undistorted_video(self):
        return self.__list_frame_undistorted_video

    @list_frame_undistorted_video.setter
    def list_frame_undistorted_video(self, value):
        self.__list_frame_undistorted_video = value

    @property
    def list_perspective_video(self):
        return self.__list_perspective_video

    @list_perspective_video.setter
    def list_perspective_video(self, value):
        self.__list_perspective_video = value

    @property
    def list_union_original_video(self):
        return self.__list_union_original_video

    @list_union_original_video.setter
    def list_union_original_video(self, value):
        self.__list_union_original_video = value

    @property
    def bird_view_video(self):
        return self.__bird_view_video

    @bird_view_video.setter
    def bird_view_video(self, value):
        self.__bird_view_video = value

    @property
    def properties_video(self):
        """
            This function is for get properties video
        Returns:
            properties video
        """
        return self.__properties_video

    @properties_video.setter
    def properties_video(self, value):
        """
            This function us for set properties video
        Args:
            value: properties video
        Returns:
            None
        """
        self.__properties_video = value
