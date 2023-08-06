def verify_deps_0():
    import lib_dep_pkg_insomniapx
    assert lib_dep_pkg_insomniapx.file0.px_psw_func_0() == 'qiqi:520 from px_psw_func_0'
    boy = lib_dep_pkg_insomniapx.file0.px_psw_cls_0()
    assert boy.get_val() == 'qiqi:520 from px_psw_cls_0'
    import lib_dep_pkg_katiezhao
    assert lib_dep_pkg_katiezhao.file0.katie_psw_func_0() == 'xiaogege:520 from katie_psw_func_0'
    girl = lib_dep_pkg_katiezhao.file0.katie_psw_cls_0()
    assert girl.get_val() == 'xiaogege:520 from katie_psw_cls_0'

def verify_deps_1():
    import lib_dep_pkg_insomniapx
    assert lib_dep_pkg_insomniapx.folder1.file1.px_psw_func_1() == 'qiqi:520 from px_psw_func_1'
    boy = lib_dep_pkg_insomniapx.folder1.file1.px_psw_cls_1()
    assert boy.get_val() == 'qiqi:520 from px_psw_cls_1'
    import lib_dep_pkg_katiezhao
    assert lib_dep_pkg_katiezhao.folder1.file1.katie_psw_func_1() == 'xiaogege:520 from katie_psw_func_1'
    girl = lib_dep_pkg_katiezhao.folder1.file1.katie_psw_cls_1()
    assert girl.get_val() == 'xiaogege:520 from katie_psw_cls_1'


def verify_deps_2():
    import lib_dep_pkg_insomniapx
    assert lib_dep_pkg_insomniapx.folder2.file2.px_psw_func_2() == 'qiqi:520 from px_psw_func_2'
    boy = lib_dep_pkg_insomniapx.folder2.file2.px_psw_cls_2()
    assert boy.get_val() == 'qiqi:520 from px_psw_cls_2'
    import lib_dep_pkg_katiezhao
    assert lib_dep_pkg_katiezhao.folder2.file2.katie_psw_func_2() == 'xiaogege:520 from katie_psw_func_2'
    girl = lib_dep_pkg_katiezhao.folder2.file2.katie_psw_cls_2()
    assert girl.get_val() == 'xiaogege:520 from katie_psw_cls_2'


def verify_deps_3():
    import lib_dep_pkg_insomniapx
    assert lib_dep_pkg_insomniapx.folder1.subfolder1.file3.px_psw_func_3() == 'qiqi:520 from px_psw_func_3'
    boy = lib_dep_pkg_insomniapx.folder1.subfolder1.file3.px_psw_cls_3()
    assert boy.get_val() == 'qiqi:520 from px_psw_cls_3'
    import lib_dep_pkg_katiezhao
    assert lib_dep_pkg_katiezhao.folder1.subfolder1.file3.katie_psw_func_3() == 'xiaogege:520 from katie_psw_func_3'
    girl = lib_dep_pkg_katiezhao.folder1.subfolder1.file3.katie_psw_cls_3()
    assert girl.get_val() == 'xiaogege:520 from katie_psw_cls_3'


def verify_deps():
    verify_deps_0()
    verify_deps_1()
    verify_deps_2()
    verify_deps_3()


class px_cal_cls:
    def __init__(self, val):
        verify_deps()
        import numpy
        a = numpy.array([0,1,3,4])
        self.val = val + a[0]
    def get_val(self):
        return self.val
    def double_self(self):
        self.val *= 2

def px_double_func(input1):
    verify_deps()
    import numpy as np
    a = np.array([i for i in range(10)])
    return input1*a[2]
