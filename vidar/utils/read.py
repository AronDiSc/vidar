# TRI-VIDAR - Copyright 2022 Toyota Research Institute.  All rights reserved.

import pickle as pkl
import json

import numpy as np
from PIL import Image

from vidar.utils.decorators import iterate1


def read_pickle(filename):
    """
    Read pickle file

    Parameters
    ----------
    filename : String
        File to read from

    Returns
    -------
    data : Value
        Data loaded from file
    """
    if not filename.endswith('.pkl'):
        filename += '.pkl'
    return pkl.load(open(filename, 'rb'))


def read_json(filename):
    """
    Read json file

    Parameters
    ----------
    filename : String
        File to read from

    Returns
    -------
    data : Value
        Data loaded from file
    """
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def read_txt(file):
    """
    Read txt file as list of lines

    Parameters
    ----------
    file : String
        Txt file filename (.txt)

    Returns
    -------
    lines: List of strings of each line in textfile
    """
    with open(file, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


@iterate1
def read_image(path):
    """
    Read an image using PIL

    Parameters
    ----------
    path : String
        Path to the image

    Returns
    -------
    image : PIL Image
        Loaded image
    """
    return Image.open(path)


@iterate1
def read_depth(file):
    """
    Load a depth map from file

    Parameters
    ----------
    file : String
        Depth map filename (.npz or .png or .dpt)

    Returns
    -------
    depth : np.array
        Depth map (invalid pixels are 0) [H,W]
    """
    # If loading a .npz array
    if file.endswith('npz'):
        return np.load(file)['depth']
    # If loading a .png image
    elif file.endswith('png'):
        depth_png = np.array(read_image(file), dtype=int)
        assert (np.max(depth_png) > 255), 'Wrong .png depth file'
        return depth_png.astype(np.float) / 256.
    # Invalid type
    else:
        raise NotImplementedError('Depth extension not supported.')

