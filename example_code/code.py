# %%
"""
# Project Setup
"""

# %% [markdown]
# $$  
# \frac{arg 1}{arg 2} \\
# x^2\\
# e^{i\pi}\\
# A_i\\
# B_{ij}\\
# \sqrt[n]{arg}	
# $$


# %%
if True:
    from itertools import combinations 
    from itertools import count
    from collections import Counter # frequency count

    import sys
    from os import remove, getcwd, makedirs, listdir, rename, rmdir, system, chdir
    from os.path import isabs, isfile, isdir, join, dirname, basename, exists, splitext, relpath

    import random

    import include

    import numpy
    import numpy as np
    from numpy.linalg import pinv as inverse
    from numpy import transpose, subtract, array, ndarray, true_divide as divide
    from numpy import matmul as matrix_multiply
    from numpy import identity as identity_matrix
    flatten = ndarray.flatten

    import pandas as pd

    import matplotlib.pyplot as plt

    from plotnine import *

    import seaborn as sns

    from scipy.stats import pearsonr

    from sklearn.linear_model import LogisticRegression


# %%
# detect if in a notebook or not
if True:
    try:
        __file__
    except NameError:
        # This is a hardcoded path because python notebooks 
        # don't support basic functionality like importing code relative
        # to the filepath of the notebook
        # https://stackoverflow.com/questions/12544056/how-do-i-get-the-current-ipython-jupyter-notebook-name
        PROJECT_PATH = "/Users/jeffhykin/Nextcloud/Programming/csce-633"
        __file__ = PROJECT_PATH+"/hw3/"
    # go to wherever this file is
    chdir(dirname(__file__))
    sys.path.append(getcwd())
    random.seed(42069)
    q1 = pd.read_csv("./data.nosync/Q1_Data.csv")
    train      = pd.read_csv("./data.nosync/Q2_Train_Data_fixed.csv")
    test       = pd.read_csv("./data.nosync/Q2_Test_Data_fixed.csv")
    validation = pd.read_csv("./data.nosync/Q2_Validation_Data_fixed.csv")

    def dev(obj):
        for each in obj.__dir__():
            print(each)

    def average(iterable):
        return sum(iterable) / len(iterable)   

# %%
if True:
    size_of_images = (48,48)
    emotions_types = { 0:"Angry", 1:"Disgust", 2:"Fear", 3:"Happy", 4:"Sad", 5:"Surprise", 6:"Neutral" }
    def get_images_and_emtions(dataframe):
        images = [ numpy.reshape(each[1:], size_of_images) for each in dataframe.to_numpy() ]
        emotions = dataframe.iloc[:, 0]
        return emotions, images

    sns.set()

# %%
"""
## 2. a: Visualize
"""
# %%
if True:
    emotions, images = get_images_and_emtions(train)
    for each_type_of_emotion in emotions_types:
        counter = 0
        print('\n#')
        print(f'# {emotions_types[each_type_of_emotion]}')
        print('#')
        for each_emotion, each_image in zip(emotions, images):
            if each_emotion == each_type_of_emotion:
                counter += 1
                plt.imshow(each_image)
                plt.show()
                if counter == 2:
                    break


# %%
"""
## 2. b: Count
"""
# %%
count = dict(Counter([ emotions_types[each] for each in emotions]))
for each in count:
    print(f'{each}: {count[each]}')
    
# %%
"""
## 2. c.0: Preprocess Images
"""
# %%
if True:
    # FIXME: basic image preprocessing in the same way as https://www.tensorflow.org/api_docs/python/tf/image/per_image_standardization. You can use Numpy and not necessarily use this function. Ignoring this step will easily result in a training failure or a significant performance decay. 

    def normalize(numerical_data):
        array_data = array(numerical_data)
        all_elements = flatten(array_data)
        max_value = max(all_elements)
        min_value = min(all_elements)
        print('max_value = ', max_value)
        print('min_value = ', min_value)
        range_value = (max_value - min_value)*1.0
        scaled_average = average(all_elements) / range_value
        print('scaled_average = ', scaled_average)
        return subtract(divide(array_data, range_value), scaled_average)

    normalized_images = normalize(images)


# %%
if True:


    import torch
    import torch.nn as nn
    import torch.optim as optimizers 
    from torch.nn import CrossEntropyLoss
    from torch.nn import Linear as FullyConnectedLayer
    from torch.nn import Conv2d as ConvolutionalLayer
    from torch.nn.functional import max_pool2d, relu
    from torch.autograd import Variable
    import torch
    import torchvision
    import torchvision.transforms as transforms

    image_size = 48 * 48 # pixels
    number_of_emotions = 6

    def generate_FNN(
            inputs,
            outputs,
            layer_sizes=[120, 84],
            learning_rate=0.001,
            momentum=9,
            number_of_epochs=2,
        ):

        class Net(nn.Module):
                
            def __init__(self):
                # call parent constructor
                super(Net, self).__init__()
                self.layers = []
                
                # 
                # First
                # 
                self.layers.append(
                    FullyConnectedLayer(
                        in_features= image_size,
                        out_features= layer_sizes.pop(),
                    )
                )
                
                # 
                # Middle
                # 
                for each_size in layer_sizes:
                    self.layers.append(
                        FullyConnectedLayer(
                            in_features= self.layers[-1].out_features,
                            out_features= each_size,
                        )
                    )
                    
                # 
                # Last
                # 
                self.layers.append(
                    FullyConnectedLayer(
                        in_features= self.layers[-1].out_features,
                        out_features= number_of_emotions,
                    )
                )
                
                # looks like pytorch is really hacky and needs the
                # layers to be saved directly on self (instead of inside a list)
                # so dynamically generate variable names to attach them
                # __l1__ for layer 1
                # __l2__ for layer 2
                # etc
                for each_number, each_layer in enumerate(self.layers):
                    self.__setattr__(f'__l{each_number}__', each_layer)
                
                # 
                # setup
                # 
                self.loss_function = CrossEntropyLoss()
                

            def forward(self, image):
                # pytorch get aNgRy if its a double (or integer) instead of a float
                activations = Variable(torch.from_numpy(numpy.array(image).astype(numpy.float32)))
                for each in self.layers:
                    activations = relu(each(activations))
                
                return activations
            
            def train_with(self, inputs, outputs):
                # 
                # setup the optimizer 
                # 
                # (can't be done inside __init__ , not sure why parameters aren't available there)
                self.optimizer = optimizers.SGD(
                    self.parameters(),
                    lr=learning_rate,
                    momentum=momentum
                )
                
                # loop over the dataset multiple times
                for epoch in range(number_of_epochs):

                    running_loss = 0.0
                    for mini_batch_number, data in enumerate(zip(outputs, inputs), 1):
                        correct_outputs, inputs = data

                        # zero the parameter gradients
                        net.optimizer.zero_grad()

                        # forward + backward + optimize
                        outputs = net.forward(inputs)
                        loss = net.loss_function(outputs, correct_outputs)
                        loss.backward()
                        net.optimizer.step()

                        # print statistics every 2000 mini-batches
                        running_loss += loss.item()
                        if mini_batch_number % 2000 == 1:
                            print('[%d, %5d] loss: %.3f' % (epoch, mini_batch_number, running_loss / 2000))
                            running_loss = 0.0
                
                print('Finished Training')
        
        
        net = Net()
        
        # FIXME: train+validate
        
        return net

    net = generate_FNN([],[])
# net.forward([0]*2304)
# %%



import sys
import logging
import traceback
import os
from os.path import isabs, isfile, isdir, join, dirname, basename, exists, splitext, relpath
from os import remove, getcwd, makedirs, listdir, rename, rmdir, system
from shutil import move
from itertools import count
import glob
import regex as re
import numpy as np
import numpy
import pickle
import random
import itertools
import time
import subprocess
from subprocess import call
import json
from pathlib import Path
import cv2 as cv
import cv2
import yaml
import colorama

# make colors work on windows
colorama.init()
# from ruamel.yaml import RoundTripLoader, RoundTripDumper, load, dump
PROJECT_ROOT = dirname(dirname(__file__))
sys.path.append(PROJECT_ROOT)

# access non existant keys without errors
class SafeList(list):
    def __getitem__(self,arg):
        try:
            return super().__getitem__(arg)
        except:
            return None
            
class ConsoleClass:
    def __init__(self):
        self.args = SafeList(sys.argv)
        # remove the system's added argument
        self.args.pop(0)
        self.foreground_colors = {  
            "black"          : 30,
            "red"            : 31,
            "green"          : 32,
            "yellow"         : 33,
            "blue"           : 34,
            "magenta"        : 35,
            "cyan"           : 36,
            "white"          : 37,
            "bright_black"   : 90,
            "bright_red"     : 91,
            "bright_green"   : 92,
            "bright_yellow"  : 93,
            "bright_blue"    : 94,
            "bright_magenta" : 95,
            "bright_cyan"    : 96,
            "bright_white"   : 97,
        }
        self.background_colors = {
            "black"          : 40,
            "red"            : 41,
            "green"          : 42,
            "yellow"         : 43,
            "blue"           : 44,
            "magenta"        : 45,
            "cyan"           : 46,
            "white"          : 47,
            "bright_black"   : 100,
            "bright_red"     : 101,
            "bright_green"   : 102,
            "bright_yellow"  : 103,
            "bright_blue"    : 104,
            "bright_magenta" : 105,
            "bright_cyan"    : 106,
            "bright_white"   : 107,
        }
    
    @property
    def arguments(self):
        return self.args
    
    def progress(self, percent=0, width=30, additional_text=""):
        percent = int(percent)
        left = width * percent // 100
        right = width - left
        print(
            '\r[', '#' * left, ' ' * right, ']',
            f' {percent:.0f}% ',
            additional_text,
            sep='',
            end='',
            flush=True
        )
    
    def get_foreground(self, color_name):
        if color_name not in self.foreground_colors:
            raise Exception(f"couldn't find foreground color_name {color_name} in: {self.foreground_colors}")
        return self.foreground_colors[color_name]
    
    def get_background(self, color_name):
        if color_name not in self.background_colors:
            raise Exception(f"couldn't find background_color color_name {color_name} in: {self.background_colors}")
        return self.background_colors[color_name]
    
    def start_color(self, foreground="white", background="black"):
        return print(f'\033[{self.get_foreground(foreground)}m\033[{self.get_background(background)}m',end="",flush=True)

    def stop_color(self, foreground="white", background="black"):
        return print(f'\033[0m',end="",flush=True)

    def color(self, string, foreground="white", background="black"):
        return f'\033[{self.get_foreground(foreground)}m\033[{self.get_background(background)}m{string}\033[0m'

Console = ConsoleClass()

import os
import glob
import shutil
class FileSystem():
    @classmethod
    def write(self, data, to=None):
        # make sure the path exists
        FileSystem.makedirs(os.path.dirname(to))
        with open(to, 'w') as the_file:
            the_file.write(str(data))
    
    @classmethod
    def read(self, filepath):
        try:
            with open(filepath,'r') as f:
                output = f.read()
        except:
            output = None
        return output    
        
    @classmethod
    def delete(self, filepath):
        if isdir(filepath):
            shutil.rmtree(filepath)
        else:
            try:
                os.remove(filepath)
            except:
                pass
    
    @classmethod
    def makedirs(self, path):
        try:
            os.makedirs(path)
        except:
            pass
        
    @classmethod
    def copy(self, from_=None, to=None, new_name="", force= True):
        if new_name == "":
            raise Exception('FileSystem.copy() needs a new_name= argument:\n    FileSystem.copy(from_="location", to="directory", new_name="")\nif you want the name to be the same as before do new_name=None')
        elif new_name is None:
            new_name = os.path.basename(from_)
        
        # get the full path
        to = os.path.join(to, new_name)
        # if theres a file in the target, delete it
        if force and FileSystem.exists(to):
            FileSystem.delete(to)
        # make sure the containing folder exists
        FileSystem.makedirs(os.path.dirname(to))
        if os.path.isdir(from_):
            shutil.copytree(from_, to)
        else:
            return shutil.copy(from_, to)
    
    @classmethod
    def move(self, from_=None, to=None, new_name="", force= True):
        if new_name == "":
            raise Exception('FileSystem.move() needs a new_name= argument:\n    FileSystem.move(from_="location", to="directory", new_name="")\nif you want the name to be the same as before do new_name=None')
        elif new_name is None:
            new_name = os.path.basename(from_)
        
        # get the full path
        to = os.path.join(to, new_name)
        # make sure the containing folder exists
        FileSystem.makedirs(os.path.dirname(to))
        shutil.move(from_, to)
    
    @classmethod
    def exists(self, *args):
        return FileSystem.does_exist(*args)
    
    @classmethod
    def does_exist(self, path):
        return os.path.exists(path)
    
    @classmethod
    def is_folder(self, *args):
        return FileSystem.is_directory(*args)
        
    @classmethod
    def is_dir(self, *args):
        return FileSystem.is_directory(*args)
        
    @classmethod
    def is_directory(self, path):
        return os.path.isdir(path)
    
    @classmethod
    def is_file(self, path):
        return os.path.isfile(path)

    @classmethod
    def list_files(self, path="."):
        return [ FS.basename(x) for x in FileSystem.ls(path) if FileSystem.is_file(x) ]

    @classmethod
    def list_filepaths(self, path="."):
        return [ x for x in FileSystem.ls(path) if FileSystem.is_file(x) ]
    
    @classmethod
    def list_folders(self, path="."):
        return [ FS.basename(x) for x in FileSystem.ls(path) if FileSystem.is_folder(x) ]

    @classmethod
    def list_folderpaths(self, path="."):
        return [ x for x in FileSystem.ls(path) if FileSystem.is_folder(x) ]
    
    @classmethod
    def ls(self, filepath="."):
        glob_val = filepath
        if os.path.isdir(filepath):
            glob_val = os.path.join(filepath, "*")
        return glob.glob(glob_val)

    @classmethod
    def touch(self, path):
        FileSystem.makedirs(FileSystem.dirname(path))
        if not FileSystem.exists(path):
            FileSystem.write("", to=path)
    
    @classmethod
    def touch_dir(self, path):
        FileSystem.makedirs(path)
    
    @classmethod
    def dirname(self, path):
        return os.path.dirname(path)
    
    @classmethod
    def basename(self, path):
        return os.path.basename(path)
    
    @classmethod
    def extname(self, path):
        filename, file_extension = os.path.splitext(path)
        return file_extension
    
    @classmethod
    def path_pieces(self, path):
        """
        example:
            *folders, file_name, file_extension = FileSystem.path_pieces("/this/is/a/filepath.txt")
        """
        folders = []
        while 1:
            path, folder = os.path.split(path)

            if folder != "":
                folders.append(folder)
            else:
                if path != "":
                    folders.append(path)

                break
        folders.reverse()
        *folders, file = folders
        filename, file_extension = os.path.splitext(file)
        return [ *folders, filename, file_extension ]
    
    @classmethod
    def join(self, *paths):
        return os.path.join(*paths)
    
    @classmethod
    def absolute_path(self, path):
        return os.path.abspath(path)
    
    @classmethod
    def generate_unique_file_name(self, base_name):
        *folders, file_name, file_extension = self.path_pieces(base_name)
        front = self.join(*folders, file_name)
        ending = file_extension
        number = 0
        name_choice = front + str(number) + ending
        while self.does_exist(name_choice):
            number += 1
            name_choice = front + str(number) + ending
        return name_choice

FS = FileSystem

#
# pulling in info
#
from copy import deepcopy

def recursively_update(old_data, new_data):
    x = old_data
    y = new_data
    z = {}
    overlapping_keys = x.keys() & y.keys()
    for key in overlapping_keys:
        # merge lists
        if type(x[key]) == list and type(y[key]) == list:
            try:
                z[key] = deepcopy(x[key])
            except expression as identifier:
                z[key] = x[key]
            # add all the new values from y
            z[key] += [ each_y for each_y in y[key] if each_y not in x[key] ]
        elif type(x[key]) == dict and type(y[key]) == dict:
            z[key] = recursively_update(x[key], y[key])
        else:
            z[key] = y[key]
    for key in x.keys() - overlapping_keys:
        try:
            z[key] = deepcopy(x[key])
        except:
            z[key] = x[key]
    for key in y.keys() - overlapping_keys:
        try:
            z[key] = deepcopy(y[key])
        except expression as identifier:
            z[key] = y[key]
    return z

import yaml
def load_info_from(info_dir):
    #
    # load info.yaml
    #
    try:
        with open(join(info_dir,"info.yaml"),'r') as f:
            yaml_string = f.read()
    except:
        yaml_string = None
    info_as_dict = yaml.unsafe_load(yaml_string)
    # load the info.yaml and some of its data
    paths = info_as_dict["(project)"]["(paths)"]
    # make paths absolute if they're relative
    for each_key in paths.keys():
        *folders, name, ext = FS.path_pieces(paths[each_key])
        # if there are no folders then it must be a relative path (otherwise it would start with the roo "/" folder)
        if len(folders) == 0:
            folders.append(".")
        # if not absolute, then make it absolute
        if folders[0] != "/":
            # remove the optional 'relative' tool 
            if folders[0] == '.' or folders[0] == './':
                _, *folders = folders
            paths[each_key] = FS.absolute_path(FS.join(PROJECT_ROOT, *folders, name+ext))
    
    # replace paths with the resolved paths
    info_as_dict["(project)"]["(paths)"] = paths
    #
    # load info.nosync.yaml
    #
    try:
        with open(join(info_dir,"info.nosync.yaml"),'r') as f:
            yaml_string = f.read()
    except:
        yaml_string = "{}" # empty hash
    
    nosync_info_as_dict = yaml.unsafe_load(yaml_string)
    # merge the values, with a preference towards the 
    info_as_dict = recursively_update(info_as_dict, nosync_info_as_dict)
    return info_as_dict

Info = load_info_from(PROJECT_ROOT)
paths = Info["(project)"]["(paths)"]
PARAMETERS = Info["parameters"]

# 
# tools for degbugging
# 
DEBUG = True
LOG_INDENT = 0
def increment_log_indent():
    global LOG_INDENT
    LOG_INDENT += 1

def decrement_log_indent():
    global LOG_INDENT
    LOG_INDENT -= 1

def log(*args, **kwargs):
    indent = LOG_INDENT * "    "
    if DEBUG == True:
        print(indent, *args, **kwargs)


from collections.abc import Iterable
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def cross_validate(data, labels, train_and_validate_function, number_of_folds=6):
    import numpy as np
    """
    data:
        needs to have its first dimension (the len()) be the number of data points
    labels:
        needs to be the same length as data
    train_and_validate_function:
        needs to have 4 arguments, train_data, train_labels, test_data, and test_labels
        it should return accuracy information as output
    number_of_folds:
        needs to be a number
    """
    # check number of folds
    if (len(data) % number_of_folds):
        # remove data until the shape fits
        data = data[:-(len(data) % number_of_folds)]
        # raise Exception("The data needs to be divisible by the number of folds")
    
    results = []
    batch_size = int(len(data) / number_of_folds)
    for batch_number in range(number_of_folds):
        print("\nOn fold:",batch_number+1)
        start_index =  batch_number      * batch_size
        end_index   = (batch_number + 1) * batch_size
        test_data   = data[start_index:end_index]
        test_labels = labels[start_index:end_index]
        
        # create data
        train_data_part_1 = data[0:start_index]
        train_data_part_2 = data[end_index:len(data)-1]
        if train_data_part_1 == []:
            train_data = train_data_part_2
        elif train_data_part_2 == []:
            train_data = train_data_part_1
        else:
            train_data   = np.concatenate((  train_data_part_1,   train_data_part_2))
        # create labels
        train_labels_part_1 = labels[0:start_index]
        train_labels_part_2 = labels[end_index:len(data)-1]
        if train_labels_part_1 == []:
            train_labels = train_labels_part_2
        elif train_labels_part_2 == []:
            train_labels = train_labels_part_1
        else:
            train_labels   = np.concatenate((  train_labels_part_1,   train_labels_part_2))
        # train and save the result
        results.append(train_and_validate_function(train_data, train_labels, test_data, test_labels))
    return results

def large_pickle_load(file_path):
    import pickle
    import os
    max_bytes = 2**31 - 1
    bytes_in = bytearray(0)
    input_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f_in:
        for _ in range(0, input_size, max_bytes):
            bytes_in += f_in.read(max_bytes)
    return pickle.loads(bytes_in)

def large_pickle_save(variable, file_path):
    import pickle
    bytes_out = pickle.dumps(variable, protocol=4)
    max_bytes = 2**31 - 1
    with open(file_path, 'wb') as f_out:
        for idx in range(0, len(bytes_out), max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])

def ndarray_to_list(ndarray):
    if type(ndarray) != numpy.ndarray:
        return ndarray
    else:
        as_list = ndarray.tolist()
        new_list = []
        for each in as_list:
            new_list.append(ndarray_to_list(each))
        return new_list



class Image(object):
    def __init__(self, arg1):
        """
        @arg1: can either be a string (the path to an image file) or an ndarray (a cv2 image)
        """
        self.face_boxes = None
        if type(arg1) == str:
            self.path = arg1
            self.img = cv.imread(arg1)
        elif type(arg1) == numpy.ndarray:
            self.path = None
            self.img = arg1
        else:
            raise Exception('Not sure how to create an image using ' + str(arg1))
    
    def find_faces(self):
        face_cascade = cv.CascadeClassifier(paths["haarcascade_frontalface_default"])
        faces = face_cascade.detectMultiScale(
            self.img,
            scaleFactor=1.1,
            minNeighbors=1,
            minSize=(100, 100),
            flags=cv.CASCADE_SCALE_IMAGE
        )
        self.face_boxes = ndarray_to_list(faces)
        return self.face_boxes
    
    def show(self):
        print("Press ESC (on the image window) to exit the image")
        if self.path != None:
            name = self.path
        else:
            name = "img"
        cv2.imshow(name, self.img)
        while True:
            key = cv2.waitKey(1)
            if key == 27:  #ESC key to break
                break
        cv2.destroyWindow(name)

    def bounding_boxes(self, color=(255, 255, 00)):
        """
        color: a tuple such as (255, 255, 00)
        returns:
            a copy of the image with the bounding boxes
        """
        img_copy = self.img.copy()
        if self.face_boxes is None:
            self.find_faces()
        for x, y, w, h in self.face_boxes:
            cv2.rectangle(img_copy, (x, y), (x+w, y+h), color, 2)
        return Image(img_copy)
    
    def with_points(self, array_of_points, color=(255, 255, 00), radius=3):
        img_copy = self.img.copy()
        for x, y, in array_of_points:
            cv.circle(img_copy, (x, y), radius, color, thickness=-1, lineType=8, shift=0)
        return Image(img_copy)
    
    def save(self, to, image_type="png"):
        FS.makedirs(FS.dirname(to))
        result = cv2.imwrite(FS.absolute_path(to+"."+image_type), self.img)
        if not result:
            raise Exception("Could not save image:"+str(to))

class Video(object):
    def __init__(self, path=None):
        self.path = path
        self.frame_generator = None
        self.largest_index_plus_1 = None
        self.frame_cache = {}
        self.CACHE_SIZE = 400 # frames
        if path is None:
            raise Exception("you're creating a Video(), but the first argument (path) is None")

    def save_frame(self, at_time, to):
        quality = "2" # can be 1-31, lower is higher quality
        call(["ffmpeg", "-ss", at_time, '-i', self.path , "-vframes", "1", "-q:v", quality, to])
        
    def get_frame(self, index):
        # init frame_generator
        if self.frame_generator is None:
            self.frame_generator = enumerate(self.frames)
        
        # don't restart from the begining of the video (aka a for loop), instead pickup where we left off 
        while 1:
            # if frame is cached, then just return it (otherwise iterate until it IS cached)
            if index in self.frame_cache:
                return self.frame_cache[index]
            
            # asked for out-of-bounds frame (not known until all frames have been iterated)
            if (self.largest_index_plus_1 is not None) and index >= self.largest_index_plus_1:
                return None
            
            # retrive the frame from the video itself
            try:
                next_index, next_frame = self.frame_generator.__next__()
            # if just went past the last frame:
            #    loop back around to the begining again (reset the generator)
            #    record the largest index
            #    don't allow the invalid frame to be cached (continue instead)
            except StopIteration:
                self.largest_index_plus_1 = index
                self.frame_generator = enumerate(self.frames)
                next_index = index + 1
                next_frame = None
                continue
            
            # if frame cache is full, delete the oldest cached frame
            if len(self.frame_cache) > self.CACHE_SIZE:
                oldest_cached_index = list(self.frame_cache.keys())[0]
                del self.frame_cache[oldest_cached_index]
            
            # cache the just-visited frame
            self.frame_cache[next_index] = next_frame

    def frames(self):
        """
        returns: a generator, where each element is a image as a numpyarray 
        """
        # Path to video file 
        video_capture = cv2.VideoCapture(self.path)
        # Check if video opened successfully
        if (video_capture.isOpened()== False): 
            raise Exception(f"Error, tried opening {self.path} with cv2 but wasn't able to")
        
        # checks whether frames were extracted 
        success = 1
        while True: 
            # function extract frames 
            success, image = video_capture.read()
            if not success:
                video_capture.release()
                return None
            yield image
        
    
    def save_with_labels(self, list_of_labels, to=None):
        # 
        # extract video data
        # 
        video_capture = cv2.VideoCapture(self.path)
        frame_width  = int(video_capture.get(3))
        frame_height = int(video_capture.get(4))
        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver) < 3:
            fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = video_capture.get(cv2.CAP_PROP_FPS)
        video_capture.release()
        
        # 
        # create new video source
        # 
        frame_dimensions = (frame_width, frame_height)
        if to is None:
            *folders, name, ext = FS.path_pieces(self.path)
            output_file = FS.join(*folders, name+".labelled"+ext)
        else:
            output_file = to
        new_video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_dimensions)
        # Read until video is completed
        for each_frame, each_label in zip(self.frames(), list_of_labels):
            if each_frame is None:
                break
            # Write text to frame
            text = str(each_label)
            text_location = (100, 100)
            font = cv2.FONT_HERSHEY_SIMPLEX
            thickness = 1
            color = (255, 255, 255)
            new_video.write(cv2.putText(each_frame, text, text_location, font, thickness, color, 2, cv2.LINE_AA))
        
        # combine the resulting frames into a video
        new_video.release()
        
import requests
class VideoDatabase(object):
    def __init__(self, url=PARAMETERS["database"]["url"]):
        self.url = url
    
    def all(self):
        return self.safe_json_post(self.url+"/all", {})
        
    def get(self, *key_list):
        return self.safe_json_post(self.url+"/get", { "keyList": key_list })

    def merge(self, *key_list, with_):
        return self.safe_json_post(self.url+"/merge", { "keyList": key_list, "value": with_ })
        
    def set(self, *key_list, to):
        return self.safe_json_post(self.url+"/set", { "keyList": key_list, "value": to })

    def delete(self, *key_list):
        return self.safe_json_post(self.url+"/delete", { "keyList": key_list})
    
    def size(self):
        return self.safe_json_post(self.url+"/size", {})
    
    def keys(self):
        return self.safe_json_post(self.url+"/keys", {})

    def eval(self, func_name, args):
        return self.safe_json_post(self.url+"/eval", {
            "key": str(func_name),
            "args": args,
        })

    def find(self, data):
        return self.safe_json_post(self.url+"/find", data)

    def grab(self, search_filter, return_filter):
        return self.safe_json_post(self.url+"/grab", {"searchFilter": search_filter, "returnFilter": return_filter})
    
    def sample(self, quantity, filter):
        return self.safe_json_post(self.url+"/sample", {"quantity": quantity, "filter": filter})
    
    def __getitem__(self, *args):
        # keys will end up always being the list of elements inside
        # the []'s of ThisClass()["<video_id>", "next_key"]
        # this is an annoying workaround of python's poortly designed edgecase behavior
        keys = args[0]
        if type(keys) == tuple:
            keys = list(keys)
        else:
            keys = [keys]
            
        return self.get(*keys)

    def __setitem__(self, *args):
        # keys will end up always being the list of elements inside
        # the []'s of ThisClass()["<video_id>", "next_key"]
        # this is an annoying workaround of python's poortly designed edgecase behavior
        keys = args[0]
        value = args[1]
        if type(keys) == tuple:
            keys = list(keys)
        else:
            keys = [keys]
        return self.set(*keys, to=value)
    
    def json_post(self, url, a_dict):
        return requests.post(url, json=a_dict)
    
    def safe_json_post(self, url, a_dict):
        data = self.json_post(url, {"args":a_dict, "key": PARAMETERS["database"]["key"]}).json()
        value = data.get("value", None)
        error = data.get("error", None)
        if error != None:
            raise Exception(f"\n\nError from database server: {error}\ndata sent: {a_dict}")
        
        return value

DB = VideoDatabase()


class DatabaseVideo(Video):
    def __init__(self, id=None):
        self.id = id
        self._data = None
        self.processing_time = 0
        self.timer_start = None
        self.frame_generator = None
        self.largest_index_plus_1 = None
        self.frame_cache = {}
        self.CACHE_SIZE = 400 # frames

    @classmethod
    def _lookup_table_of_cached_videos(self):
        all_paths = FS.list_filepaths(paths["video_cache"])
        video_id_hash = {}
        for each in all_paths:
            *parent_dirs, file_name, file_ext = FS.path_pieces(each)
            if file_ext == ".mp4":
                video_id = FS.extname(file_name)
                # cutoff the .
                video_id = video_id[1:]
                # associate the id with a filepath
                video_id_hash[video_id] = each
                
        return video_id_hash
    
    @classmethod
    def _get_cached_video_path(self, video_id):
        all_paths = FS.list_filepaths(paths["video_cache"])
        video_path = DatabaseVideo._lookup_table_of_cached_videos().get(video_id, None)
        if video_path is None:
            return None
        else:
            return video_path
        return None

    @classmethod
    def _download_video(self, video_id):
        video_path = DatabaseVideo._get_cached_video_path(video_id)
        if video_path is None:
            print(Console.color(f'A video {video_id} wasn\'t avalible locally, downloading it now', foreground="blue"))
            # run the downloader
            url = str("https://www.youtube.com/watch?v="+video_id)
            path_to_video = FS.join(paths["video_cache"], f"name.{video_id}.mp4")
            return_code = call(["youtube-dl", url, "-f", 'bestvideo[ext=mp4]', "-o" , path_to_video])
            if return_code is not 0:
                raise Exception(f'Download of youtube video {video_id} failed')
            # will return null if there was a download error
            return DatabaseVideo._get_cached_video_path(video_id)
        else:
            return video_path

    # TODO: fix this as it appears python doesn't like it when it has a class method and a property with the same name
    @classmethod
    def url(self, video_id):
        return "https://www.youtube.com/watch?v=" + video_id
    
    def start_timer():
        self.timer_start = time.time()
    
    @property
    def data(self):
        self.timer_start = time.time()
        
        # if data hasn't been retrived, then 
        if self._data == None:
            self._data = DB[self.id]
            
        self.processing_time += time.time() - self.timer_start
        return self._data
    
    def merge_data(self, new_data):
        self.timer_start = time.time()
        
        if self._data == None:
            self._data = DB[self.id]
        self._data = recursively_update(self._data, new_data=new_data)
        # update the database
        DB[self.id] = self._data
        self.processing_time += time.time() - self.timer_start
    
    @property
    def url(self):
        return DatabaseVideo.url(self.id)
    
    @property
    def path(self):
        return DatabaseVideo._lookup_table_of_cached_videos().get(self.id, None)
    
    @property
    def frames(self):
        # download it if needed
        DatabaseVideo._download_video(self.id)
        if self.path is None or self.path is "":
            raise Exception(f'Video {self.id} couldn\'t be found after downloading it')
        return super().frames()
    
    def __getitem__(self, *args):
        self.timer_start = time.time()
        
        # keys will end up always being the list of elements inside
        # the []'s of ThisClass()["<video_id>", "next_key"]
        # this is an annoying workaround of python's poortly designed edgecase behavior
        keys = args[0]
        if type(keys) == tuple:
            keys = list(keys)
        else:
            keys = [keys]
        
        list_copy = [ self.id ] + keys
        output = DB[tuple(list_copy)]
        
        self.processing_time += time.time() - self.timer_start
        return output
    
    def __setitem__(self, *args):
        self.timer_start = time.time()
        
        # keys will end up always being the list of elements inside
        # the []'s of ThisClass()["<video_id>", "next_key"]
        # this is an annoying workaround of python's poortly designed edgecase behavior
        keys = args[0]
        value = args[1]
        if type(keys) == tuple:
            keys = list(keys)
        else:
            keys = [keys]
            
        list_copy = [ self.id ] + keys
        # set that value
        DB[tuple(list_copy)] = value
        
        self.processing_time += time.time() - self.timer_start

# needs re, FS, DB, Video, and Info
class VideoSelect(object):
    """
    if you need to retrive videos already stored on the disk 
    or if you need to retrive videos that meet a specific metadata requirement
    or if you need to pop a video off of a priority stack
    this tool is the right one for the job
    
    videos will be downloaded as-needed
    
    To get a generator for all videos do: 
        videos = VideoSelect().retrive()
    
    To get a generator for all downloaded videos do:
        videos = VideoSelect().is_downloaded.retrive()
    
    """
    
    class Any(object): # use as a substitute
        pass
    
    def __init__(self):
        self.db_query_stack = [{}]
    
    def _add_query_restriction(self, new_restriction):
        # prefer the first restriction when there's a conflict
        self.db_query_stack[-1] = recursively_update(new_restriction, self.db_query_stack[-1])
    
    def retrive(self):
        already_seen_videos = set()
        # create a generator function that spits out video objects one at a time
        for each_query in self.db_query_stack:
            results_of_query = set(DB.find(each_query))
            # this only cares about the keys (video id's)
            unseen_videos = results_of_query - already_seen_videos 
            for each_video_id in unseen_videos:
                # output full objects
                yield DatabaseVideo(each_video_id)
            # all the unseen have now been seen
            already_seen_videos |= unseen_videos

    @property
    def then(self):
        # create a new stack
        self.db_query_stack.append({})
        return self
        
    @property
    def has_basic_info(self):
        self._add_query_restriction({ "basic_info" : { "$exists": True } })
        return self

    @property
    def has_related_videos(self):
        # has at least 1 related video
        self._add_query_restriction({ "related_videos": { "$exists": True, "$not": {"$size": 0} }})
        return self
    
    @property
    def is_downloaded(self):
        # lookup the id's of all the cached videos
        prefered_ids = []
        lookup_table = DatabaseVideo._lookup_table_of_cached_videos()
        prefered_ids = lookup_table.keys()
        if len(prefered_ids) > 0:
            # add them as a restriction
            self._add_query_restriction({ "_id" : { "$in": list(prefered_ids) } })
        else:
            # remove the current query because it is impossible to meet the requirements of
            # (impossible because there are no download videos)
            self.db_query_stack.pop()
        return self

import sys
import os
from os.path import isabs, isfile, isdir, join, dirname, basename, exists, splitext
from os import remove, getcwd, makedirs, listdir, rename, rmdir
from shutil import move
import dlib
import glob
import numpy as np

detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(paths["shape_predictor_68_face_landmarks"])

nuber_of_face_features = 68

import math
def average(items):
    running_total = 0
    for each in items:
        running_total += each
    return running_total / len(items)

class Geometry():
    @classmethod
    def bounds_to_points(self, max_x, max_y, min_x, min_y):
        return (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, min_y)
    
    @classmethod
    def bounding_box(self, array_of_points):
        """
        the input needs to be an array with the first column being x values, and the second column being y values
        """
        max_x = -float('Inf')
        max_y = -float('Inf')
        min_x = float('Inf')
        min_y = float('Inf')
        for each in array_of_points:
            if max_x < each[0]:
                max_x = each[0]
            if max_y < each[1]:
                max_y = each[1]
            if min_x > each[0]:
                min_x = each[0]
            if min_y > each[1]:
                min_y = each[1]
        return max_x, max_y, min_x, min_y
    
    @classmethod
    def poly_area(self, points):
        """
        @points: a list of points (x,y tuples) that form a polygon
        
        returns: the aread of the polygon
        """
        xs = []
        ys = []
        for each in points:
            x,y = each
            xs.append(x)
            ys.append(y)
        return 0.5*np.abs(np.dot(xs,np.roll(ys,1))-np.dot(ys,np.roll(xs,1)))


    @classmethod
    def distance_between(self, point1, point2):
        x1,y1 = point1
        x2,y2 = point2
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        return dist  

    @classmethod
    def rotate(self, point, angle, about):
        """
        @about a tuple (x,y) as a point, this is the point that will be used as the axis of rotation
        @point a tuple (x,y) as a point that will get rotated counter-clockwise about the origin
        @angle an angle in radians, the amount of counter-clockwise roation

        The angle should be given in radians.
        """
        ox, oy = about
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
    
    @classmethod
    def counter_clockwise_angle(self, from_, to):
        x1, y1 = from_
        x2, y2 = to
        answer = math.atan2(x1*y2-y1*x2,x1*x2+y1*y2)
        # if negative, change to positive and add 180 degrees
        if answer < 0:
            answer = answer * -1 + math.pi
        return answer
    
    @classmethod
    def vector_pointing(self, from_, to):
        return tuple(map(int.__sub__, to, point))

class Face():
    def __init__(self, shape=None, img=None, as_array=None):
        global nuber_of_face_features
        if as_array is None:
            self.img = img
            # create the empty array
            self.as_array = np.empty((nuber_of_face_features, 2), dtype=np.int32)
            self.relative_face = None
            # store the face as an array
            for each_part_index in range(shape.num_parts):
                point = shape.part(each_part_index)
                self.as_array[each_part_index][0] = point.x
                self.as_array[each_part_index][1] = point.y
        else:
            self.as_array = as_array
        
        # calculate the bounding boxes
        self.chin_curve_bounds    = Geometry.bounding_box(self.chin_curve())
        self.left_eyebrow_bounds  = Geometry.bounding_box(self.left_eyebrow())
        self.right_eyebrow_bounds = Geometry.bounding_box(self.right_eyebrow())
        self.nose_bounds          = Geometry.bounding_box(self.nose())
        self.left_eye_bounds      = Geometry.bounding_box(self.left_eye())
        self.right_eye_bounds     = Geometry.bounding_box(self.right_eye())
        self.mouth_bounds         = Geometry.bounding_box(self.mouth())
        # calculate the face bounding box
        max_x = max(self.chin_curve_bounds[0], self.left_eyebrow_bounds[0], self.right_eyebrow_bounds[0], self.nose_bounds[0], self.left_eye_bounds[0], self.right_eye_bounds[0], self.mouth_bounds[0])
        max_y = max(self.chin_curve_bounds[1], self.left_eyebrow_bounds[1], self.right_eyebrow_bounds[1], self.nose_bounds[1], self.left_eye_bounds[1], self.right_eye_bounds[1], self.mouth_bounds[1])
        min_x = min(self.chin_curve_bounds[2], self.left_eyebrow_bounds[2], self.right_eyebrow_bounds[2], self.nose_bounds[2], self.left_eye_bounds[2], self.right_eye_bounds[2], self.mouth_bounds[2])
        min_y = min(self.chin_curve_bounds[3], self.left_eyebrow_bounds[3], self.right_eyebrow_bounds[3], self.nose_bounds[3], self.left_eye_bounds[3], self.right_eye_bounds[3], self.mouth_bounds[3])
        self.bounds = ( max_x, max_y, min_x, min_y )
    
    def bounded_by(self, bounds, padding):
        height = self.img.shape[0]
        x_max = bounds[0] + int(padding * height)
        y_max = bounds[1] + int(padding * height)
        x_min = bounds[2] - int(padding * height)
        y_min = bounds[3] - int(padding * height)
        # dont let the indices go negative
        if x_min < 0:
            x_min = 0
        if y_min < 0:
            y_min = 0
        return self.img[ y_min:y_max, x_min:x_max]
    
    #
    # Facial parts
    #
    # see: https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png
    def chin_curve(self):
        return self.as_array[0:16]
    def left_eyebrow(self):
        return self.as_array[17:21]
    def right_eyebrow(self):
        return self.as_array[22:26]
    def nose(self):
        return self.as_array[27:35]
    def left_eye(self):
        return self.as_array[36:41]
    def right_eye(self):
        return self.as_array[42:47]
    def mouth(self):
        return self.as_array[48:67]

    #
    # bounding boxes
    #
    def bounding_box(self):
        return Geometry.bounds_to_points(*self.bounds)
    def chin_curve_bounding_box(self):
        return Geometry.bounds_to_points(*self.chin_curve_bounds)
    def left_eyebrow_bounding_box(self):
        return Geometry.bounds_to_points(*self.left_eyebrow_bounds)
    def right_eyebrow_bounding_box(self):
        return Geometry.bounds_to_points(*self.right_eyebrow_bounds)
    def nose_bounding_box(self):
        return Geometry.bounds_to_points(*self.nose_bounds)
    def left_eye_bounding_box(self):
        return Geometry.bounds_to_points(*self.left_eye_bounds)
    def right_eye_bounding_box(self):
        return Geometry.bounds_to_points(*self.right_eye_bounds)
    def mouth_bounding_box(self):
        return Geometry.bounds_to_points(*self.mouth_bounds)
    
    #
    # Save options
    #
    def save_to(self, image_path, padding):
        """padding is a percentage of the height"""
        dlib.save_image(self.bounded_by(self.bounds, padding), image_path)
    def save_chin_curve_to(self, image_path, padding):
        """padding is a percentage of the height"""
        dlib.save_image(self.bounded_by(self.chin_curve_bounds, padding), image_path)
    def save_left_eyebrow_to(self, image_path, padding):
        """padding is a percentage of the height"""
        dlib.save_image(self.bounded_by(self.left_eyebrow_bounds, padding), image_path)
    def save_right_eyebrow_to(self, image_path, padding):
        """padding is a percentage of the height"""
        dlib.save_image(self.bounded_by(self.right_eyebrow_bounds, padding), image_path)
    def save_nose_to(self, image_path, padding):
        """padding is a percentage of the height"""
        dlib.save_image(self.bounded_by(self.nose_bounds, padding), image_path)
    def save_left_eye_to(self, image_path, padding):
        """padding is a percentage of the height"""
        dlib.save_image(self.bounded_by(self.left_eye_bounds, padding), image_path)
    def save_right_eye_to(self, image_path, padding):
        """padding is a percentage of the height"""
        dlib.save_image(self.bounded_by(self.right_eye_bounds, padding), image_path)
    def save_mouth_to(self, image_path, padding):
        """padding is a percentage of the height"""
        dlib.save_image(self.bounded_by(self.mouth_bounds, padding), image_path)
    
    # 
    # misc helpers
    #
    def bottom_of_chin():
        # these magic indexes are from: https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png
        return self.as_array[0]
    
    def top_of_nose(self):
        # these magic indexes are from: https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png
        return self.as_array[16]
    
    def face_relative_points(self):
        # TODO: this could be done more efficiently with a single matrix multiplication (2D rotate, translate, scale)
        
        # performs a roation on each point to make the face vertical
        # translates the face so that the center of the chin is (0,0)
        # scales the points relative to the width/height of the face 
        
        global nuber_of_face_features
        if self.relative_face != None:
            return self.relative_face
        
        faces_vector = Geometry.vector_pointing(from_=self.bottom_of_chin(), to=self.top_of_nose())
        base_vector  = (0,1)
        # note: this angle will probably be more than 180 degrees
        # this is because its putting the face on a mathematical plane (y increases as it goes up)
        # and the image plane y gets larger going down
        needed_rotation = Geometry.counter_clockwise_angle(from_=face_vector, to=base_vector)
        
        # create the empty array for the new face points
        self.relative_face = np.empty((nuber_of_face_features, 2), dtype=np.int32)
        # rotate the chin-point first to get the new origin
        new_bottom_of_chin_x, new_bottom_of_chin_y  = Geometry.rotate(point=self.bottom_of_chin(), angle=needed_rotation, about=(0,0))
        # get width and height for scaling
        width, height = (self.width(), self.height())
        for each_index, each_point in enumerate(self.as_array):
            each_x, each_y = each_point
            # perform the rotation
            new_point_x, new_point_y = Geometry.rotate(point=each_point, angle=needed_rotation, about=(0,0))
            # perform the translation (to make the chin the new origin)
            new_point_x, new_point_y = ( new_point_x - new_bottom_of_chin_x, new_point_y - new_bottom_of_chin_y )
            # perform the scaling
            new_scaled_point = ( new_point_x / width, new_point_y / height )
            
            self.relative_face = new_scaled_point
        
        return self.relative_face
        
    # this is the width from one side of the face to the other side
    def width(self):
        # these magic indexes are from: https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png
        return Geometry.distance_between(self.as_array[0], self.as_array[16])
    
    # this is the height from the top of the nose to the bottom of the chin
    def height(self):
        # these magic indexes are from: https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png
        return Geometry.distance_between(self.as_array[8], self.as_array[27])
        
    def mouth_openness(self):
        """
        
        """
        # for reference see: https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png
        distance_1 = Geometry.distance_between(self.as_array[61], self.as_array[67])
        distance_2 = Geometry.distance_between(self.as_array[62], self.as_array[66])
        distance_3 = Geometry.distance_between(self.as_array[63], self.as_array[65])
        return average([distance_1, distance_2, distance_3])
    
    def eye_width(self):
        # for reference see: https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png
        right_eye_width  = Geometry.distance_between(self.right_eye()[0], self.right_eye()[-3])
        left_eye_width   = Geometry.distance_between(self.left_eye()[0] , self.left_eye()[-3])
        return average([right_eye_width, left_eye_width])
    
    def left_eye_center(self):
        eye_points = self.left_eye()
        average_x = average([ point[0] for point in eye_points ])
        average_y = average([ point[1] for point in eye_points ])
        return ( average_x, average_y )

    def right_eye_center(self):
        eye_points = self.right_eye()
        average_x = average([ point[0] for point in eye_points ])
        average_y = average([ point[1] for point in eye_points ])
        return ( average_x, average_y )
        
    def eyebrow_raise_score(self, left_right_or_both="both"):
        """
        left_right_or_both: a string that is either "left", "right", or "both" depending on the desired eyebrow height
        
        returns a float representing how high the eyebrows are raised
        """
            
        if left_right_or_both == "left":
            eye_points = self.left_eye()
            eyebrow_points = self.left_eyebrow()
            center_of_eye = self.left_eye_center()
        elif left_right_or_both == "right":
            eye_points = self.right_eye()
            eyebrow_points = self.right_eyebrow()
            center_of_eye = self.right_eye_center()
        else:
            # recursively get each side
            standardized_height_of_left  = self.eyebrow_raise_score(left_right_or_both="left")
            standardized_height_of_right = self.eyebrow_raise_score(left_right_or_both="right")
            
            # penalize for being different
            # explaination:
            #     if they're only a little different (relative to their overall height)
            #     then most of that difference will be added (close to a max(height_left, height_right) )
            #     if they're very different relative to their overall height above the eye
            #     then most of that difference will not be added (close to a min(height_left, height_right) )
            difference = abs(standardized_height_of_left - standardized_height_of_right)
            similarity = min(standardized_height_of_left, standardized_height_of_right)
            percent_similar = difference / similarity
            moderated_value = similarity + (difference * percent_similar)
            return moderated_value
            
        eyebrow_height = average([ Geometry.distance_between(center_of_eye, each_eyebrow_point) for each_eyebrow_point in eyebrow_points ])
        standardized_eyebrow_height = eyebrow_height / self.eye_width()
        
        return standardized_eyebrow_height
        
        # # Alternative method
        # get the eye points as if the eye was closed (crush down to only 4 points)
        # for reference see: https://miro.medium.com/max/828/1*96UT-D8uSXjlnyvs9DZTog.png
        # eye_points = (
        #     eye_points[0],
        #     (eye_points[1] + eye_points[-1])/2,
        #     (eye_points[2] + eye_points[-2])/2,
        #     eye_points[-3]
        # )
        # # use this to create a genertic value
        # eye_width  = Geometry.distance_between(eye_points[0], eye_points[-1])
        
        # TODO: get the nose vector instead of using distance
        # np.dot(x, y) / np.linalg.norm(y)
        
        # sum the distance
        # running_height = 0
        # for each_eye_point in eye_points:
        #     # get the average distance of the eyebrow points
        #     avg_distance = average([ Geometry.distance_between(each_eye_point, each_eyebrow_point) for each_eyebrow_point in eyebrow_points ])
        #     running_height += avg_distance
        # # divide to get the average
        # eyebrow_height = running_height / len(sides_of_eye)


def faces_for(img):
    global detector
    global predictor

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)
    # initialize by the number of faces
    faces = [None]*len(dets)
    for index, d in enumerate(dets):
        faces[index] = Face(predictor(img, d), img)

    return faces

def aligned_faces_for(img, size=320, padding=0.25):
    images = get_aligned_face_images(img, size, padding)
    faces = [None]*len(images)
    for each_index, each_img in enumerate(images):
        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.
        dets = detector(each_img, 1)
        # initialize by the number of faces
        faces = [None]*len(dets)
        for d in dets:
            faces[each_index] = Face(predictor(each_img, d), each_img)
    return faces


def get_aligned_face_images(img, size=320, padding=0.25):
    global detector
    global predictor

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)

    # if no faces return an empty list
    if len(dets) == 0:
        return []

    # Find the 5 face landmarks we need to do the alignment.
    faces = dlib.full_object_detections()
    for detection in dets:
        faces.append(predictor(img, detection))

    # returns a list of images
    return dlib.get_face_chips(img, faces, size=size, padding=padding)


def vector_points_for(jpg_image_path):
    global detector
    global predictor

    # load up the image
    img = dlib.load_rgb_image(jpg_image_path)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)

    # initialize by the number of faces
    faces = [None]*len(dets)
    for index, d in enumerate(dets):
        shape = predictor(img, d)
        # copy over all 68 facial features/vertexs/points
        faces[index] = [ shape.part(each_part_index) for each_part_index in range(shape.num_parts) ]

    return faces
    
    
