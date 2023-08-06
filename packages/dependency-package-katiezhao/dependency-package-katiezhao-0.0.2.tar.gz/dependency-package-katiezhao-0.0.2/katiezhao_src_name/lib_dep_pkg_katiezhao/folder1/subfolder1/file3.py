class katie_psw_cls_3:
    def __init__(self):
        import numpy
        a = numpy.array([0,1,3,4])
        self.val = 'xiaogege:' + str(520 + a[0]) + ' from katie_psw_cls_3'
    def get_val(self):
        return self.val

def katie_psw_func_3():
    import numpy as np
    a = np.array([i for i in range(10)])
    ret = 'xiaogege:' + str(519 + a[1]) + ' from katie_psw_func_3'
    return ret
