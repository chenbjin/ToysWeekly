# -*- encoding: utf8 -*-
# author: chenbjin
# time: 2018/03/18 23:11:44

# character type 
NUMBER   = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
UP_CASE  = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
LOW_CASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# captcha config
CAPTCHA_LIST   = NUMBER + LOW_CASE + UP_CASE
CAPTCHA_LEN    = 4
CAPTCHA_HEIGHT = 60
CAPTCHA_WIDTH  = 160

# model config
INPUT_SHAPE = (CAPTCHA_HEIGHT, CAPTCHA_WIDTH, 1)
BATCH_SIZE  = 64
EPOCHS      = 30
