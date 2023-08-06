import cv2 as cv
import numpy as np
from cvbot._sift import find, show_features


def _mse(imga, imgb):
    err = np.sum((imga.astype("float") - imgb.astype("float")) ** 2)
    err /= float(imga.shape[0] * imga.shape[1])

    return err

def _cmse(imga, imgb):
    return (_mse(imga[:, :, 0], imgb[:, :, 0]) + 
            _mse(imga[:, :, 1], imgb[:, :, 1]) +
            _mse(imga[:, :, 2], imgb[:, :, 2]))

def sift_find(temp, scene, quality):
    """
    Image, Image, int -> box
    Find using sift features of the image 'temp' in 'scene' image and return the location as a rectangle/box
            quality : minimum features to find
    """
    return find(temp.grey(),
                scene.grey(), quality)

def sift_feats(img):
    """
    Image -> None
    Show detected sift feature of 'img' in a window on screen
    """
    show_features(img.grey())

def mse(imga, imgb):
    """
    Image, Image -> float | None
    Return the mean squared difference between two images
    """
    if imga.type != imgb.type:
        print("Mean squared difference cannot be calculated with images of different color types")
    elif imga.type == "grey":
        return _mse(imga.img, imgb.img) 
    else:
        return _cmse(imga.img, imgb.img)
