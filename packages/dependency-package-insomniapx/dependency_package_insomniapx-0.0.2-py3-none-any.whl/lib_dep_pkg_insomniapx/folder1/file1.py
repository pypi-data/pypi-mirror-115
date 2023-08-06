class px_psw_cls_1:
    def __init__(self):
        import numpy
        a = numpy.array([0,1,3,4])
        self.val = 'qiqi:' + str(520 + a[0]) + ' from px_psw_cls_1'
    def get_val(self):
        return self.val

def px_psw_func_1():
    import numpy as np
    a = np.array([i for i in range(10)])
    ret = 'qiqi:' + str(519 + a[1]) + ' from px_psw_func_1'
    return ret