# -*- encoding: utf8 -*-
# author: chenbjin
# time: 2018/03/25 14:03:10

import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from keras.models import load_model

from utils import load_image
from utils import revert_to_char_label

def break_captcha(model, img_path, default_model='convnet'):
    """Recognize captcha from img_path"""
    x = load_image(img_path)
    pred = model.predict(x)
    label = revert_to_char_label(pred)
    print label
    return label[0]

if __name__ == '__main__':
    model = load_model('my_model.h5')
    img_path = 'captcha_img/captcha_2-hnMM.jpg'
    break_captcha(model, img_path)
