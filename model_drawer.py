from vpython import box, color, sphere, vector
from data import Model
import itertools


class ModelDrawer:
    # map descriptions of models to values suitable for use in vpython
    vpython_function_map = {"box": box, "sphere": sphere}
    size_kwarg_map = {"box": "size", "sphere": "radius"}
    size_derivation_map = None  # assign this later; needs access to static variables in the same class
    size_map = {"small": 0.7, "big": 1.2}
    radius_map = {"small": 0.4, "big": 0.8}
    color_map = {"red": color.red, "green": color.green}

    # initialize a model drawer by giving it a model to draw
    def __init__(self, model):
        self.model = model

    # derive the vpython function and the kwargs that go with it, then call it
    def draw(self):
        vpython_function = self.derive_vpython_function()
        vpython_kwargs = self.derive_vpython_kwargs()
        vpython_function(**vpython_kwargs)

    # match the name of the shape with the vpython function that draws it
    # example: "box" -> box
    def derive_vpython_function(self):
        return self.vpython_function_map[self.model.shape]

    # derive each kwarg, and put it in a dict
    def derive_vpython_kwargs(self):
        return {self.derive_size_kwarg(): self.call_size_derivation_function(), "color": self.derive_color(),
                "pos": self.derive_pos()}

    # match the name of the shape with the size kwarg that we need
    # example: "box" -> "size", but "sphere" -> "radius"
    def derive_size_kwarg(self):
        return self.size_kwarg_map[self.model.shape]

    # match the name of the shape with the function that derives its size
    # example: "box" -> derive_size, but "sphere" -> derive_radius
    def call_size_derivation_function(self):
        return self.size_derivation_map[self.model.shape](self)

    # derives the vector-size of a box based on a verbal description of its size
    # example: "small" -> 0.7 -> vector(0.7, 0.7, 0.7)
    def derive_size(self):
        size_value = self.size_map[self.model.size]
        size_args = [size_value] * 3
        size = vector(*size_args)
        return size

    # derives the radius of the sphere based on a verbal description of its size
    # example: "big" -> 0.8
    def derive_radius(self):
        return self.radius_map[self.model.size]

    # derives the vector-color (RGB) of the model based on the name of the color
    # example: "red" -> color.red -> vector(1, 0, 0)
    def derive_color(self):
        return self.color_map[self.model.color]

    # derives the vector-position of the model based on its location on the 3x3 grid
    # example: (0, 0, 0) -> vector(0, 0, 0)
    def derive_pos(self):
        return vector(*self.model.vpython_location)

    @staticmethod
    def generate_permutations():
        sizes = ModelDrawer.size_map.keys()
        colors = ModelDrawer.color_map.keys()
        shapes = ModelDrawer.vpython_function_map.keys()
        return list(itertools.product(sizes, colors, shapes))

    @staticmethod
    def model_tuples_to_models(model_tuples):
        models = []
        for model_tuple in model_tuples:
            model = Model()
            model.size = model_tuple[0]
            model.color = model_tuple[1]
            model.shape = model_tuple[2]
            models.append(model)
        return models


# we are assigning a static variable that uses other static variables of the class
# so, we can't actually perform this assignment until the class was already initialized
ModelDrawer.size_derivation_map = {"box": ModelDrawer.derive_size, "sphere": ModelDrawer.derive_radius}
