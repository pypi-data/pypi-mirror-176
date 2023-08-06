import numpy as np


# https://discovery.ucl.ac.uk/id/eprint/10146893/1/geometry_medim.pdf

def affine_matrix(
    image_orientation, 
    image_position, 
    pixel_spacing, 
    slice_spacing):

    row_spacing = pixel_spacing[0]
    column_spacing = pixel_spacing[1]

    row_cosine = np.array(image_orientation[:3])
    column_cosine = np.array(image_orientation[3:])
    slice_cosine = np.cross(row_cosine, column_cosine)

    affine = np.identity(4, dtype=np.float32)
    affine[:3, 0] = row_cosine * column_spacing
    affine[:3, 1] = column_cosine * row_spacing
    affine[:3, 2] = slice_cosine * slice_spacing
    affine[:3, 3] = image_position
    
    return affine 


def clip(array, value_range = None):

    array[np.isnan(array)] = 0
    if value_range is None:
        finite = array[np.isfinite(array)]
        value_range = [np.amin(finite), np.amax(finite)]
    return np.clip(array, value_range[0], value_range[1])
    

def scale_to_range(array, bits_allocated):
        
    range = 2.0**bits_allocated - 1
    maximum = np.amax(array)
    minimum = np.amin(array)
    if maximum == minimum:
        slope = 1
    else:
        slope = range / (maximum - minimum)
    intercept = -slope * minimum
    array *= slope
    array += intercept

    if bits_allocated == 8:
        return array.astype(np.uint8), slope, intercept
    if bits_allocated == 16:
        return array.astype(np.uint16), slope, intercept
    if bits_allocated == 32:
        return array.astype(np.uint32), slope, intercept
    if bits_allocated == 64:
        return array.astype(np.uint64), slope, intercept


def BGRA(array, RGBlut=None, width=None, center=None):

    if (width is None) or (center is None):
        max = np.amax(array)
        min = np.amin(array)
    else:
        max = center+width/2
        min = center-width/2

    # Scale pixel array into byte range
    array = np.clip(array, min, max)
    array -= min
    if max > min:
        array *= 255/(max-min)
    array = array.astype(np.ubyte)

    BGRA = np.empty(array.shape[:2]+(4,), dtype=np.ubyte)
    BGRA[:,:,3] = 255 # Alpha channel

    if RGBlut is None:
        # Greyscale image
        for c in range(3):
            BGRA[:,:,c] = array
    else:
        # Scale LUT into byte range
        RGBlut *= 255
        RGBlut = RGBlut.astype(np.ubyte)       
        # Create RGB array by indexing LUT with pixel array
        for c in range(3):
            BGRA[:,:,c] = RGBlut[array,2-c]

    return BGRA




