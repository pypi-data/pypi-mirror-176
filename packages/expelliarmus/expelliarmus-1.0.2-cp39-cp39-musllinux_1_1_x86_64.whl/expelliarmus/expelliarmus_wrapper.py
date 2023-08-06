import os
import pathlib
import re
from ctypes import *
from typing import Optional, Union

import numpy as np
from numpy.lib.recfunctions import unstructured_to_structured

# Stuff you do not need to worry about :)

# Searching for the shared library.
this_file_path = pathlib.Path(__file__).resolve().parent.parent
lib_re = r"^expelliarmus\..*\.(so|pyd)$"
for root, dirs, files in os.walk(this_file_path):
    for f in files:
        if re.match(lib_re, f):
            lib_path = pathlib.Path(os.path.join(root, f))
            break
c_lib_expelliarmus = CDLL(str(lib_path))

# Setting up C wrappers.
ARGTYPES_READ = [c_char_p, POINTER(c_size_t), c_size_t]
RESTYPE_READ = POINTER(c_ulonglong)

c_read_dat = c_lib_expelliarmus.read_dat
c_read_evt2 = c_lib_expelliarmus.read_evt2
c_read_evt3 = c_lib_expelliarmus.read_evt3
for c_read_fn in (c_read_dat, c_read_evt2, c_read_evt3):
    c_read_fn.restype = RESTYPE_READ
    c_read_fn.argtypes = ARGTYPES_READ

ARGTYPES_CUT = [c_char_p, c_char_p, c_size_t, c_size_t]
RESTYPE_CUT = c_size_t

c_cut_dat = c_lib_expelliarmus.cut_dat
c_cut_evt2 = c_lib_expelliarmus.cut_evt2
c_cut_evt3 = c_lib_expelliarmus.cut_evt3
for c_cut_fn in (c_cut_dat, c_cut_evt2, c_cut_evt3):
    c_cut_fn.restype = RESTYPE_CUT
    c_cut_fn.argtypes = ARGTYPES_CUT

# Default data type for structured array.
DTYPE = np.dtype([("t", np.int64), ("x", np.int16), ("y", np.int16), ("p", np.uint8)])

def c_read_wrapper(p_fun, fpath, buff_size, dtype):
    assert isinstance(fpath, str) or isinstance(fpath, pathlib.Path)
    fpath = pathlib.Path(fpath).resolve()
    assert fpath.is_file(), f'Error: the file provided "{str(fpath)}" does not exist.'
    assert isinstance(buff_size, int) and buff_size > 0, "Error: a minimum buffer size of 1 is required."

    c_fpath = c_char_p(bytes(str(fpath), "utf-8"))
    c_dim = c_size_t(0)
    c_buff_size = c_size_t(buff_size)
    if p_fun == read_dat:
        c_arr = c_read_dat(c_fpath, byref(c_dim), c_buff_size)
    elif p_fun == read_evt2:
        c_arr = c_read_evt2(c_fpath, byref(c_dim), c_buff_size)
    elif p_fun == read_evt3:
        c_arr = c_read_evt3(c_fpath, byref(c_dim), c_buff_size)
    else:
        raise "Function not defined."
    np_arr = np.ctypeslib.as_array(c_arr, shape=(c_dim.value,)).reshape(
        (c_dim.value // 4, 4)
    )
    np_arr = unstructured_to_structured(np_arr, dtype=dtype)
    return np_arr


def c_cut_wrapper(p_fun, fpath_in, fpath_out, new_duration, buff_size):
    assert isinstance(fpath_in, str) or isinstance(fpath_in, pathlib.Path)
    assert isinstance(fpath_out, str) or isinstance(fpath_out, pathlib.Path)
    fpath_in = pathlib.Path(fpath_in).resolve()
    fpath_out = pathlib.Path(fpath_out).resolve()
    assert (
        fpath_in.is_file()
    ), f'Error: the input file provided "{str(fpath_in)}" does not exist.'
    assert (
        fpath_out.parent.is_dir()
    ), f'Error: the output file path provided "{str(fpath_out)}" does not exist.'
    assert isinstance(buff_size, int) and buff_size > 0, "Error: a minimum buffer size of 1 is required."
    assert isinstance(new_duration, int) and new_duration > 0, "Error: the new time duration of the recording must be larger than or equal to 1ms."

    c_fpath_in = c_char_p(bytes(str(fpath_in), "utf-8"))
    c_fpath_out = c_char_p(bytes(str(fpath_out), "utf-8"))
    c_new_duration = c_size_t(new_duration)
    c_buff_size = c_size_t(buff_size)
    if p_fun == cut_dat:
        c_dim = c_cut_dat(c_fpath_in, c_fpath_out, c_new_duration, c_buff_size)
    elif p_fun == cut_evt2:
        c_dim = c_cut_evt2(c_fpath_in, c_fpath_out, c_new_duration, c_buff_size)
    elif p_fun == cut_evt3:
        c_dim = c_cut_evt3(c_fpath_in, c_fpath_out, c_new_duration, c_buff_size)
    else:
        raise "Function not defined."
    return c_dim


# Actual stuff you should care about.


def read_dat(
    fpath: Union[pathlib.Path, str],
    buff_size: Optional[int] = 4096,
    dtype: Optional[np.dtype] = DTYPE,
) -> np.ndarray:
    """
    Function that reads a DAT binary file to a structured NumPy array.
    Args:
        - fpath: path to the DAT file.
        - buff_size: size of the buffer used to read the binary file.
        - dtype: the types for the structured array.
    Returns:
        - arr: a structured NumPy array that encodes (timestamp, x_address, y_address, polarity).
    """
    assert str(fpath).endswith(".dat"), f"Error: the file provided \"{str(fpath)}\" is not a DAT file."
    return c_read_wrapper(read_dat, fpath, buff_size, dtype)


def read_evt2(
    fpath: Union[pathlib.Path, str],
    buff_size: Optional[int] = 4096,
    dtype: Optional[np.dtype] = DTYPE,
) -> np.ndarray:
    """
    Function that reads a EVT2 binary file to a structured NumPy array.
    Args:
        - fpath: path to the EVT2 file.
        - buff_size: size of the buffer used to read the binary file.
        - dtype: the types for the structured array.
    Returns:
        - arr: a structured NumPy array that encodes (timestamp, x_address, y_address, polarity).
    """
    assert str(fpath).endswith(".raw"), "Error: the file provided \"{str(fpath)}\" is not a RAW file."
    return c_read_wrapper(read_evt2, fpath, buff_size, dtype)


def read_evt3(
    fpath: Union[pathlib.Path, str],
    buff_size: Optional[int] = 4096,
    dtype: Optional[np.dtype] = DTYPE,
) -> np.ndarray:
    """
    Function that reads a EVT3 binary file to a structured NumPy array.
    Args:
        - fpath: path to the DAT file.
        - buff_size: size of the buffer used to read the binary file.
        - dtype: the types for the structured array.
    Returns:
        - arr: a structured NumPy array that encodes (timestamp, x_address, y_address, polarity).
    """
    assert str(fpath).endswith(".raw"), "Error: the file provided \"{str(fpath)}\" is not a RAW file."
    return c_read_wrapper(read_evt3, fpath, buff_size, dtype)


def cut_dat(
    fpath_in: Union[pathlib.Path, str],
    fpath_out: Union[pathlib.Path, str],
    new_duration: Optional[int] = 10,
    buff_size: Optional[int] = 4096,
) -> int:
    """
    Function that reads a DAT binary file and cuts it to a limited number of events.
    Args:
        - fpath_in: path to the input DAT file.
        - fpath_out: path to the output DAT file.
        - new_duration: new time duration of the recording expressed in milliseconds.
        - buff_size: size of the buffer used to read the binary file.
    Returns:
        - dim: the number of events encoded in the output file.
    """
    assert str(fpath_in).endswith(".dat"), f"Error: the input file provided \"{str(fpath_in)}\" is not a DAT file."
    assert str(fpath_out).endswith(".dat"), f"Error: the output file provided \"{str(fpath_out)}\" is not a DAT file."
    return c_cut_wrapper(cut_dat, fpath_in, fpath_out, new_duration, buff_size)


def cut_evt2(
    fpath_in: Union[pathlib.Path, str],
    fpath_out: Union[pathlib.Path, str],
    new_duration: Optional[int] = 10,
    buff_size: Optional[int] = 4096,
) -> int:
    """
    Function that reads a EVT2 binary file and cuts it to a limited number of events.
    Args:
        - fpath_in: path to the input EVT2 file.
        - fpath_out: path to the output EVT2 file.
        - new_duration: new time duration of the recording expressed in milliseconds.
        - max_nevents: number of events to be written in the output file.
        - buff_size: size of the buffer used to read the binary file.
    Returns:
        - dim: the number of events encoded in the output file.
    """
    assert str(fpath_in).endswith(".raw"), f"Error: the input file provided \"{str(fpath_in)}\" is not a RAW file."
    assert str(fpath_out).endswith(".raw"), f"Error: the output file provided \"{str(fpath_out)}\" is not a RAW file."
    return c_cut_wrapper(cut_evt2, fpath_in, fpath_out, new_duration, buff_size)


def cut_evt3(
    fpath_in: Union[pathlib.Path, str],
    fpath_out: Union[pathlib.Path, str],
    new_duration: Optional[int] = 10,
    buff_size: Optional[int] = 4096,
) -> int:
    """
    Function that reads a EVT3 binary file and cuts it to a limited number of events.
    Args:
        - fpath_in: path to the input EVT3 file.
        - fpath_out: path to the output EVT3 file.
        - new_duration: new time duration of the recording expressed in milliseconds.
        - buff_size: size of the buffer used to read the binary file.
    Returns:
        - dim: the number of events encoded in the output file.
    """
    assert str(fpath_in).endswith(".raw"), f"Error: the input file provided \"{str(fpath_in)}\" is not a RAW file."
    assert str(fpath_out).endswith(".raw"), f"Error: the output file provided \"{str(fpath_out)}\" is not a RAW file."
    return c_cut_wrapper(cut_evt3, fpath_in, fpath_out, new_duration, buff_size)
