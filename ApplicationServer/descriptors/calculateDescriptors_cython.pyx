# """
# This module provides the cython implementation for the color correlogram
# feature extraction.
# 
# @copyright: Copyright 2010 Deutsches Forschungszentrum fuer Kuenstliche
#             Intelligenz GmbH or its licensors, as applicable.
# @license: This is free software: you can redistribute it and/or modify it under
#           the terms of the GNU General Public License as published by the Free
#           Software Foundation, either version 3 of the License, or (at your
#           option) any later version. You should have received a copy of the
#           GNU General Public License along with this software (COPYING).
#           If not, see <http://www.gnu.org/licenses/>.
# """
cimport numpy as np
import numpy as np

from rgb2hsy_cbased import *

cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)

def calculateDescriptors_cython(image):
    # """"
    # Calculate the color correlogram descriptors in cython.
    #
    # see CalculateDescriptors.m of Johann Hoffmann
    # image is PIL.Image
    # returns modifiedAutoCorellogram, colourHistogram, statVec
    # 
    # """"
 
    
    #----Initiate and set variables-------------------------------
    binH = 9
    binS = 5
    binL = 4

    rows = image.size[1] # weird order in PIL.Images
    columns = image.size[0]
    nrOfPxls = rows * columns

    sizeThresh = 500.0
    #-------------------------------------------------------------

    #----Pre-processing (e.g. convert colours space, resizing)----
    if ((rows >= sizeThresh) or (columns >= sizeThresh)):
        resizeRatio = min(sizeThresh / rows, sizeThresh / columns)
        newcolumns = int(round(columns * resizeRatio))
        newrows = int(round(rows * resizeRatio))

        image = image.resize((newcolumns, newrows))
        
        rows = image.size[1] # weird order in PIL.Images
        columns = image.size[0]
        nrOfPxls = rows * columns
        
    # convert into numpy array in RGB colorspace
    rgbIm = np.asarray(image.convert("RGB")) #dtype = uint8
    
    hsyIm = rgb2hsy_cbased(rgbIm)
    #-------------------------------------------------------------
    
    #----Quenatize the colour dimension---------------------------
    if ((hsyIm[:,:,1]).max() <= 1) and ((hsyIm[:,:,2]).max() <= 1):
        H = hsyIm[:,:,0] * (binH/360.0)
        L = hsyIm[:,:,2] * binL
        S = hsyIm[:,:,1] * binS
    else:
        H = hsyIm[:,:,0] * (binH / 360.0)
        L = hsyIm[:,:,2] * (binL / 255.0)
        S = hsyIm[:,:,1] * (binS / 255.0)
    hsyIm[:,:,0] = H
    hsyIm[:,:,2] = L
    hsyIm[:,:,1] = S
    #-------------------------------------------------------------   

    #----Calculate statVec----------------------------------------
    dH = np.double(hsyIm[:,:,0] / binH)
    dS = np.double(hsyIm[:,:,1] / binS)
    dL = np.double(hsyIm[:,:,2] / binL)

    meanH = np.mean(dH)

    statVec = np.zeros(6)
    statVec[0] = 0  #this value is set below
    statVec[1] = np.mean(dS) #meanS
    statVec[2] = np.mean(dL)  #meanL
    statVec[3] = np.median(dS, axis=None)  #medianS
    statVec[4] = np.sum(sum((dH - meanH) ** 2)) / nrOfPxls;  #varH
    statVec[5] = np.sum(sum((dL - statVec[2]) ** 2)) / nrOfPxls;  #varL
    #-------------------------------------------------------------

    #----Generate histograms--------------------------------------
    # cast of reals to ints 
    # TODO: check that no problems occur here
    
    cdef np.ndarray[np.uint8_t, ndim=3] hsyImC = np.uint8(hsyIm.round())
    
    cdef np.ndarray[np.float64_t, ndim=3] colourHistogram = np.zeros((binH + 1,
                                                                      binS + 1,
                                                                      binL + 1))
    cdef np.ndarray[np.float64_t, ndim=3] modifiedAutoCorrellogram = np.zeros((binH + 1, binS + 1, binL + 1))
    
    # This value represents the overall probability that any color is
    # surrounded by by pixels of the same
    cdef double corra = 0.0  
    
    cdef Py_ssize_t x,y
    cdef double surr 
    
    for x in range(3,(rows - 3)):
        for y in range(3,(columns - 3)):
            
            surr = 0.0
            
            if (hsyImC[x,y,0] == hsyImC[x-1,y,0] and hsyImC[x,y,1] == hsyImC[x-1,y,1] and hsyImC[x,y,2] == hsyImC[x-1,y,2]):
                surr = surr + 1
            if (hsyImC[x,y,0] == hsyImC[x,y-1,0] and hsyImC[x,y,1] == hsyImC[x,y-1,1] and hsyImC[x,y,2] == hsyImC[x,y-1,2]):
                surr = surr + 1                  
            if (hsyImC[x,y,0] == hsyImC[x+1,y,0] and hsyImC[x,y,1] == hsyImC[x+1,y,1] and hsyImC[x,y,2] == hsyImC[x+1,y,2]):
                surr = surr + 1            
            if (hsyImC[x,y,0] == hsyImC[x,y+1,0] and hsyImC[x,y,1] == hsyImC[x,y+1,1] and hsyImC[x,y,2] == hsyImC[x,y+1,2]):
                surr = surr + 1            
            if (hsyImC[x,y,0] == hsyImC[x-3,y-3,0] and hsyImC[x,y,1] == hsyImC[x-3,y-3,1] and hsyImC[x,y,2] == hsyImC[x-3,y-3,2]):
                surr = surr + 1  
            if (hsyImC[x,y,0] == hsyImC[x-3,y+3,0] and hsyImC[x,y,1] == hsyImC[x-3,y+3,1] and hsyImC[x,y,2] == hsyImC[x-3,y+3,2]):
                surr = surr + 1                  
            if (hsyImC[x,y,0] == hsyImC[x+3,y+3,0] and hsyImC[x,y,1] == hsyImC[x+3,y+3,1] and hsyImC[x,y,2] == hsyImC[x+3,y+3,2]):
                surr = surr + 1            
            if (hsyImC[x,y,0] == hsyImC[x+3,y-3,0] and hsyImC[x,y,1] == hsyImC[x+3,y-3,1] and hsyImC[x,y,2] == hsyImC[x+3,y-3,2]):
                surr = surr + 1   
                 
            modifiedAutoCorrellogram[hsyImC[x,y,0], hsyImC[x,y,1], hsyImC[x,y,2]] = modifiedAutoCorrellogram[hsyImC[x,y,0], hsyImC[x,y,1], hsyImC[x,y,2]] + surr / 8
            colourHistogram[hsyImC[x,y,0], hsyImC[x,y,1], hsyImC[x,y,2]] = colourHistogram[hsyImC[x,y,0], hsyImC[x,y,1], hsyImC[x,y,2]] + 1
            
            corra = corra + surr / 8
    
    statVec[0] = corra / np.real((rows - 6) * (columns - 6)) # was nrOfPxls; better: np.sum(colourHistogram) or (rows-6)*(columns-6)
    
    # idea:
    # if colorhistogram(x,y,z) != 0:
    #   modifiedAutoCorrellogram(x,y,z) = modifiedAutoCorrellogram(x,y,z) / colourHistogram(x,y,z)
    # else:
    #   modifiedAutoCorrellogram(x,y,z) = 0
    
    # faster implementation:
    
    div = colourHistogram.copy()
    div[div==0] = np.inf
    modifiedAutoCorrellogram = modifiedAutoCorrellogram / div

    colourHistogram = colourHistogram / np.real((rows - 6) * (columns - 6)) # see comment above
    #-------------------------------------------------------------
    
    return (modifiedAutoCorrellogram, colourHistogram, statVec)

