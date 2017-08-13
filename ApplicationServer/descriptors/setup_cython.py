from distutils.core import setup
from distutils.extension import Extension

from Cython.Distutils import build_ext
from numpy.distutils.misc_util import get_numpy_include_dirs

# building calculateDescriptors
ext_modules = [Extension("calculateDescriptors_cython",
                         ["calculateDescriptors_cython.pyx"],
                         get_numpy_include_dirs()
             )]

setup(
    name = 'calculateDescriptors_cython',
    cmdclass= {'build_ext': build_ext},
    ext_modules = ext_modules
)

# building rgb2hsy
ext_modules = [Extension("rgb2hsy_cbased",
                         ["rgb2hsy_cbased.pyx"],
                         get_numpy_include_dirs(),
                         libraries=["m"]
             )]

setup(
    name = 'rgb2hsy_cbased',
    cmdclass= {'build_ext': build_ext},
    ext_modules = ext_modules
)
