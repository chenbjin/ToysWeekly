# -*- encoding: utf8 -*-
# author: chenbjin
# time: 2018/03/11 15:51:39

import keras
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Dropout, Flatten, Reshape, merge
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.merge import Concatenate
from keras.layers.normalization import BatchNormalization

def convnet(input_shape, num_class):
    """简单的convnet，四个输出一起softmax，一个分类器
       训练时的acc，是4乘以num_class这么多输出的平均准确率
    """
    model_input = Input(shape=input_shape)
    # 1 conv
    conv_1 = Conv2D(64, kernel_size=(5, 9), activation='relu')(model_input)
    pool_1 = MaxPooling2D(pool_size=(2, 4))(conv_1)
    drop_1 = Dropout(0.5)(pool_1)
    # 2 conv
    conv_2 = Conv2D(64, kernel_size=(5, 7), activation='relu')(drop_1)
    pool_2 = MaxPooling2D(pool_size=(2, 4))(conv_2)
    drop_2 = Dropout(0.5)(pool_2)
    # flatten
    flat = Flatten()(drop_2)
    # output
    model_output = Dense(num_class*4, activation='softmax')(flat)
    model = Model(model_input, model_output)
    model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

def multi_convnet(input_shape, num_class, output_size=4):
    """四个输出4个softmax
    """
    
    model_input = Input(shape=input_shape)
    # 1 conv
    conv_1 = Conv2D(64, kernel_size=(5, 9), activation='relu')(model_input)
    pool_1 = MaxPooling2D(pool_size=(2, 4))(conv_1)
    drop_1 = Dropout(0.5)(pool_1)
    # 2 conv
    conv_2 = Conv2D(64, kernel_size=(5, 7), activation='relu')(drop_1)
    pool_2 = MaxPooling2D(pool_size=(2, 4))(conv_2)
    drop_2 = Dropout(0.5)(pool_2)
    # 3 conv
    conv_3 = Conv2D(32, kernel_size=(3, 5), activation='relu')(drop_2)
    pool_3 = MaxPooling2D(pool_size=(2, 2))(conv_3)
    drop_3 = Dropout(0.2)(pool_3)
    # flatten
    flat = Flatten()(drop_3)
    # output
    out = []
    for i in range(output_size):
        out.append(Dense(num_class, activation='softmax')(flat))
    model_output = out
    model = Model(inputs=model_input, outputs=model_output)
    model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model
