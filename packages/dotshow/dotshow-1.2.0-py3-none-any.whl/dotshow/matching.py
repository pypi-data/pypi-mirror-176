import numpy as np
import cv2
from sys import stdout
from .under import under_sampling, under_sampling_color
from .weight import weight_match
from .weight import color_match

def dotshow(arr, gray=False, size=7):
    d_arr, real = under_sampling(arr, size=size)
    print("__"*real[0])
    print(d_arr.shape)
    for line in d_arr:
        print("|", end="")
        for var in line:
            val = weight_match(var, gray)
            print(val, end=" ")
        print("|")
    print("__"*real[0])

def __stdshow__(arr, gray=False, size=7):
    d_arr, real = under_sampling(arr, size=size)
    stdout.write("__"*real[0]+"\n")
    for line in d_arr:
        stdout.write("|")
        for var in line:
            val = weight_match(var, gray)
            stdout.write(val+" ")
        stdout.write("|"+"\n")
    stdout.write("__"*real[0]+"\n")

def loadshow(path, gray=False, size=7, color=True):
    img = cv2.imread(path)
    if color:
        colorshow(img, size=size)
    else:
        dotshow(img, gray, size)

def colorshow(arr, size=7):
    d_arr, real = under_sampling_color(arr, size=size)
    print("__"*real[0])
    for line in d_arr:
        print("|", end="")
        for var in line:
            val = color_match(var)
            print(val, end=" ")
        print("|")
    print("__"*real[0])