import warnings
from functools import wraps
from itertools import tee

import numpy as np
from scipy.signal import argrelextrema


def find_nearest_value_index(array, value):
    idx = (np.abs(array-value)).argmin()
    return idx


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def print_return_value(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(func.__name__)
        print(ret)
        return ret
    return wrapper


@print_return_value
def get_local_maximas(arr, smooth_param):
    # smooth the array to get nice local maximas
    arr = smooth(
        arr, window_len=smooth_param
    )

    return argrelextrema(arr, np.greater)[0]


def slices(arr, slice_len=3):
    for i in range(len(arr) - slice_len):
        t = arr[i : i + slice_len]
        print(t.shape)
        yield t
    for i in range(len(arr) - slice_len, len(arr)):
        t = np.append(arr[i:], arr[:slice_len - (len(arr) - i)])
        print(t.shape)
        yield t


@print_return_value
def local_maximas(arr, window_len):

    arr = smooth(
        arr, window_len=window_len
    )


    if window_len % 2 == 0:
        warnings.warn('Use odd window_len')
    window_len += 1

    middle = window_len//2
    maximas = np.zeros((len(arr)))
    for i, slice in enumerate(slices(arr, window_len)):

        if slice.mean()*1.2 > slice.max():
            value = 2
        else:
            value = 1
        maximas[(i + slice.argmax()) % len(maximas)] += value

    print(maximas)
    return np.where(maximas > 14)[0]


#get_local_maximas = local_maximas


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y