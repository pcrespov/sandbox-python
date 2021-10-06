import numpy as np

def find_index(base:np.ndarray, view: np.ndarray):

    assert view.base is base
    assert view.itemsize == base.itemsize

    # bounding box in bytes (global)
    view_lower, view_upper = np.byte_bounds(view)
    base_lower, base_upper = np.byte_bounds(base)
    assert base_lower <= view_lower
    assert view_upper <= base_upper

    offset_lower = (view_lower - base_lower)// base.itemsize
    offset_upper = (base_upper - view_upper) // base.itemsize

    # strides are in bytes
    steps = [ view.strides[n] // base.strides[n] for n in range(base.ndim) ]
    assert all(steps!=0)

    slices = []
    for n in range(base.ndim):
        step = view.strides[n] // base.strides[n]
        
        if step>0:
            start = offset_lower #<<<<<<<<<<<<<<<<<<<<
            stop = offset_upper
        else:
            start = offset_upper - 1
            stop = offset_lower -1

        slices.append(slice(start, stop, step))