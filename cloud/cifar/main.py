import tensorflow as tf
from generate_dataset import generate_dataset
import numpy as np
import time
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os

CLIENT_NUMBER = 20
FAULT_INDEX = 3
FAULT_RATIO = 0.3
LOG_FOLDER = 'logs_f3e30'
IS_KMEANS = False
if IS_KMEANS:
    EXP_NAME = f'{CLIENT_NUMBER}_{FAULT_INDEX+1}_attack_{FAULT_RATIO}_kmeans'
else:
    EXP_NAME = f'{CLIENT_NUMBER}_{FAULT_INDEX+1}_attack_{FAULT_RATIO}'



(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

x_train = x_train.astype("float32") / 255.0
y_train = np.squeeze(y_train)
x_test = x_test.astype("float32") / 255.0
y_test = np.squeeze(y_test)






os.makedirs(f"./{LOG_FOLDER}/{EXP_NAME}")



def generate_cmd(fault_index=FAULT_INDEX, model_type='cnn', exp_type='local', exp_name = EXP_NAME, client_num = CLIENT_NUMBER):

    if IS_KMEANS:
        cmds = [f'python client.py -c {i} -f {fault_index} -m {model_type} -e {exp_type} -n {exp_name} -k > ./{LOG_FOLDER}/{EXP_NAME}/client_{i}_fault_{fault_index}.log' for i in range(client_num)]
    else:
        cmds = [f'python client.py -c {i} -f {fault_index} -m {model_type} -e {exp_type} -n {exp_name} > ./{LOG_FOLDER}/{EXP_NAME}/client_{i}_fault_{fault_index}.log' for i in range(client_num)]
    print(' & '.join(cmds))
    return ' & '.join(cmds)


    

generate_dataset(x_train, y_train, x_test, y_test, CLIENT_NUMBER, FAULT_INDEX, falut_ratio=FAULT_RATIO)


os.system(f"nohup python server.py > ./{LOG_FOLDER}/{EXP_NAME}/server.log 2>&1 &")

time.sleep(20)

os.system(generate_cmd())
