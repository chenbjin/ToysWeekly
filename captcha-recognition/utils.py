# -*- encoding: utf8 -*-
# author: chenbjin
# time: 2018/03/18 23:09:17

import os
import sys

import numpy as np
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from keras.preprocessing.image import img_to_array, load_img

from common import CAPTCHA_LIST, CAPTCHA_LEN, INPUT_SHAPE

def one_hot_encode(text, char_list=CAPTCHA_LIST):
    """Translation of characters to unique integer vectors"""
    ret = []
    for char in text:
        vec = np.zeros(len(char_list))
        vec[char_list.index(char)] = 1
        ret.append(vec)
    return ret

def one_hot_decode(vec, char_list=CAPTCHA_LIST):
    """Translation of vectors to characters label"""
    text = []
    for probs in vec:
        text.append(CAPTCHA_LIST[np.argmax(probs)])
    return text

def convert_to_general_target(labels, char_len=4):
    """
    Translate labels to keras general target format, which concatenate one-hot vector
    
    Args:
        labels: a list of sample's label, shape like ['BN2D','fs2n', ...]
    Return:
        y: a numpy array, shape is (len(labels), 4, 62)
    """
    labels = [one_hot_encode(label) for label in labels]
    y = [np.concatenate(label) for label in labels]
    y = np.array(y)
    return y

def convert_to_multi_output_target(labels, char_len=4):
    """
    Translate labels to keras multi-output target format, for multi-output architecture(4 softmax),
    the target is a list of 4 Numpy arrays.
    
    Args:
        labels: a list of sample's label, shape like ['BN2D','fs2n', ...]
        char_len: the len of characters of the captcha

    Return:
        y: a list of 4 Numpy arrays, shape like (4, len(labels), 62)
    """
    labels = [one_hot_encode(label) for label in labels]
    y = [[] for _ in range(char_len)]
    for label in labels:
        for idx in range(char_len):
            y[idx].append(label[idx])
    y = [arr for arr in np.array(y)]
    return y

def revert_to_char_label(preds, char_len=4, num_class=62):
    """
    Revert the output of model.predict() to characters label

    Args:
        preds: a list of 4 probability Numpy arrays, 
        char_len: the len of character label

    Return:
        labels: a list of label
    """
    labels = []
    if len(preds) == char_len:
        for idx in range(char_len):
            preds[idx] = one_hot_decode(preds[idx])
        batch_size = len(preds[0])
        for i in range(batch_size):
            label = []
            for j in range(char_len):
                label.append(preds[j][i])
            labels.append(''.join(label))
    else:
        for i in range(len(preds)):
            label = []
            for j in range(char_len):
                label.append(preds[i][num_class*j:num_class*(j+1)])
            labels.append(''.join(one_hot_decode(label)))
    return labels

def load_data(img_dir='captcha_img/'):
    """
    Load img and label from directory
    The label is split with '-', eg. "captcha_img/captcha_1234-BN3s.jpg"
    """
    data = []
    label = []
    for img in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img)
        # load the image as grayscale, and converts image to a Numpy array
        x = load_img(img_path, True)
        x = img_to_array(x)
        y = img.split('-')[1].split('.')[0]
        data.append(x)
        label.append(y)
    return [data, label]

def split_data(x, y, ratio=0.15):
    """Split data for train and test"""
    test_size = int(len(y)*ratio)
    x_test = x[:test_size]
    y_test = y[:test_size]
    x_train = x[test_size:]
    y_train = y[test_size:]
    return [x_train, y_train, x_test, y_test]

def load_image(img_path):
    data = load_img(img_path, True)
    data = img_to_array(data)
    x = np.array(data)
    x = np.expand_dims(x, axis=0)
    x = 255 - x
    x /= 255
    return x
