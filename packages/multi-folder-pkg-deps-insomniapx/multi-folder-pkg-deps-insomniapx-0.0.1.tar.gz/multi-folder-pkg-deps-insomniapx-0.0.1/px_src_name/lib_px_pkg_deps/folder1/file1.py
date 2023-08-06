class px_mul_cls:
    def __init__(self, val):
        import numpy
        a = numpy.array([0,1,3,4])
        self.val = val + a[0]
    def get_val(self):
        return self.val
    def mul(self, val_opr):
        self.val *= val_opr

def px_mul_func(input1, input2):
    import numpy as np
    a = np.array([i for i in range(10)])
    return input1*input2*a[1]
