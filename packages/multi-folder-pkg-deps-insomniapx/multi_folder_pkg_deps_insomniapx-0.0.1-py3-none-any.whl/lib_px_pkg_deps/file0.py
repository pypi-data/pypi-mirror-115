class px_cls:
    def __init__(self, val):
        import numpy
        a = numpy.array([0,1,3,4])
        self.val = val + a[0]
    def get_val(self):
        return self.val
    def add_one(self):
        self.val += 1

def px_func(input1):
    import numpy as np
    a = np.array([i for i in range(10)])
    return input1 + a[1]
