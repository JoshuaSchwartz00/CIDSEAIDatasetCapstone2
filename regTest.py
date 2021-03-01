import re
import exrex


class object: 
    size = ""
    color = ""
    shape = ""
    x = 0 #need to compare x coord for left/right
    y = 0
    z = 0
    def __init__(self, size, color, shape):
        self.size = size
        self.color = color
        self.shape = shape

def main():
    #print(exrex.generate('This is (a (code|cake|test)|an (apple|elf|output))\.'))
    #print("\n".join(exrex.generate('This is (a (color|cake|test)|an (apple|elf|output))\.')))
    print("\n".join(exrex.generate('(small|large) (red|green) (cube|sphere)')))

    c1 = object("small","red", "cube")
    c1.size
    c1dict = {
        f"{c1.size} objects" : "<size> object template",
        f"{c1.color} objects" : "<col> object template",
        f"{c1.shape}s" : "<shape> template",
        f"{c1.color} {c1.shape}s" : "<col> <shape> template",
        f"{c1.size} {c1.color} objects" : "<size> <col> object template",
        f"{c1.size} {c1.shape}s" : "<size> <shape> object template",
        f"{c1.size} {c1.color} {c1.shape}s" : "<size> <color> <shape> template",
    }
    

    print(c1dict)


thisdict = {
"" : "<col> object template",
"" : "<shape> template",
"" : "<col> <shape> template",
"" : "<size> <col> object template",
"" : "<size> <color> <shape> template",
"" : "left to x template",
"" : "x from left template"
}


main()