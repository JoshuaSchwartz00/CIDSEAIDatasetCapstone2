class Model:
    # maps vpython location to pixel location
    pixel_map = {(-2, 2, 0): (110, 86), (0, 2, 0): (250, 86), (2, 2, 0): (390, 86),
                 (-2, 0, 0): (110, 232), (0, 0, 0): (250, 232), (2, 0, 0): (390, 232),
                 (-2, -2, 0): (110, 378), (0, -2, 0): (250, 378), (2, -2, 0): (390, 378)}

    # objects can be: small or big, red or green, box or sphere
    def __init__(self):
        self.size = None
        self.color = None
        self.shape = None
        self.vpython_location = None  # a tuple (x, y, z)
        self.normalized_location = None  # origin is top-left
        self.pixel_location = None  # mapping from location -> pixel coordinates via dictionary

    def __str__(self):
        my_str = ""
        for item in vars(self):
            my_str += "{} = {}, ".format(item, getattr(self, item))
        return my_str[0:my_str.rindex(",")]

    def derive_normalized_location(self):
        normalized_x = (self.vpython_location[0] + 2) // 2
        normalized_y = (-1 * self.vpython_location[1] + 2) // 2
        self.normalized_location = (normalized_x, normalized_y)

    def derive_pixel_location(self):
        self.pixel_location = self.pixel_map[self.vpython_location]


class Scene:
    def __init__(self):
        self.image_location = None
        self.model_list = None
        self.objects_tuples = []  # info = [index, item.color, item.shape, item.size, item.location]
        self.list_expressions = []  # (ref expr, template, (1,3 if it applies to objects 1 and 3))
        self.list_segmented_image = []  # ((c1.size) objects, <size> object, segmented image path)

    def __str__(self):
        my_str = "image_location = {}\n".format(self.image_location)
        my_str += "model_list:\n"
        for model in self.model_list:
            my_str += "{}\n".format(model)
        return my_str
