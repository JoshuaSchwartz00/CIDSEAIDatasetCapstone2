class Object: 
    size = ""
    color = ""
    shape = ""
    location = (0,0,0)
    def init(self, size, color, shape, location):
        self.size = size
        self.color = color
        self.shape = shape
        self.location = location

class Scene:
    image_location = "" #filename
    list_objects = list()
    list_expressions = list() # {c1.size} objects" : ["<size> object template"]
    #{'small objects': '<size> object template', 'red objects': '<col> object template', 'cubes': '<shape> template', 'red cubes': '<col> <shape> template', 'small red objects': '<size> <col> object template', 'small cubes': '<size> <shape> object template', 'small red cubes': '<size> <color> <shape> template'}
    list_segmented_image = list() #((c1.size) objects, <size> object, segmented image path)
    def init(self):
        print("temp")


list_scenes = list()



if __name__ == "__main__":
    print("hello")