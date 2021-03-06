from tensorflow.keras.layers import Input, Conv2D, Dense, MaxPool2D, Flatten
from tensorflow.keras.models import Model, Sequential
import tensorflow as tf

mobile_net = tf.keras.applications.MobileNetV2((32, 32, 3), classes=10, weights=None)

def get_naive_cnn():
    _input = Input((28, 28, 1))
    x = Conv2D(filters=32, kernel_size=(3, 3), strides=(2, 2), activation='relu', padding='same')(_input)
    x = Conv2D(filters=64, kernel_size=(3, 3), strides=(2, 2), activation='relu', padding='same')(x)
    x = MaxPool2D((2, 2))(x)
    x = Conv2D(filters=64, kernel_size=(3, 3), strides=(2, 2), activation='relu', padding='same')(x)
    x = Conv2D(filters=32, kernel_size=(3, 3), strides=(2, 2), activation='relu', padding='same')(x)
    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(128, name='feature', activation='relu')(x)
    x = Dense(10, activation='softmax')(x)
    return Model(inputs=[_input], outputs=[x])


def get_ann():
    model = Sequential()
    model.add(Input(shape=(128, )))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    print('output shape:', model.output_shape)
    return model
