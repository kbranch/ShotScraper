class Rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
    
    def fromObj(obj):
        if hasattr(obj, '__iter__'):
            return Rectangle(obj[0], obj[1], obj[2], obj[3])
        
        return Rectangle(obj.left, obj.top, obj.right, obj.bottom)

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top
    
    def toTuple(self):
        return (self.left, self.top, self.right, self.bottom)