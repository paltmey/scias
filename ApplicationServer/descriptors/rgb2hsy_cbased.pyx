cimport numpy as np
import numpy as np
from numpy import zeros, dstack



cdef extern from "math.h":
    double sqrt(double)
    
cdef extern from "math.h":
    double acos(double)    

cdef extern from "math.h":
    double fmin(double, double)

cdef extern from "math.h":
    double fmax(double, double)

cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)


def rgb2hsy_cbased(np.ndarray[np.uint8_t, ndim=3] rgb):
    size = (rgb.shape[0],rgb.shape[1])

    cdef np.ndarray[np.float64_t, ndim=1] red = rgb[:,:,0].ravel() / 255.0
    cdef np.ndarray[np.float64_t, ndim=1] green = rgb[:,:,1].ravel() / 255.0
    cdef np.ndarray[np.float64_t, ndim=1] blue = rgb[:,:,2].ravel() / 255.0

    cdef np.ndarray[np.float64_t, ndim=1] h = zeros(rgb.shape[0]*rgb.shape[1])
    cdef np.ndarray[np.float64_t, ndim=1] s = zeros(rgb.shape[0]*rgb.shape[1])
    cdef np.ndarray[np.float64_t, ndim=1] y = zeros(rgb.shape[0]*rgb.shape[1])
    
    cdef double c=sqrt(3)/2
    cdef double C1,C2,C
    cdef double pi = 3.14159265358979323846

    cdef Py_ssize_t i
    cdef double rval, gval, bval, yval
    cdef double hval = 0.0

    for i in range(h.shape[0]):
        rval=red[i]
        gval=green[i]
        bval=blue[i]
        # H
        C1=(rval-0.5*(gval+bval))
        C2=c*(bval-gval)
        C=sqrt(C1*C1+C2*C2)
        if (C==0):
            hval=0
        elif (C2<=0):
            hval=acos(C1/C)
        elif (C2>0):
            hval=2*pi-acos(C1/C)
        
        h[i] = hval * (180.0/pi)
        
        # S
        s[i] = fmax(rval,fmax(gval,bval))-fmin(rval,fmin(gval,bval))
        # Y
        yval=0.299*rval+0.587*gval+0.114*bval
        y[i] = yval
        
    h_2d = h.reshape(size)
    s_2d = s.reshape(size)
    y_2d = y.reshape(size)
    hsy = dstack((h_2d,s_2d,y_2d))

    return hsy


