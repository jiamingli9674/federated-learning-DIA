import tensorflow as tf
from generate_dataset import generate_dataset
import numpy as np
import time
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pickle
from sklearn.model_selection import train_test_split
import os

CLIENT_NUMBER = 10
FAULT_INDEX = 7
FAULT_RATIO = 0.4


IS_KMEANS = True
if IS_KMEANS:
    EXP_NAME = f'solar_{CLIENT_NUMBER}_{FAULT_INDEX+1}_attack_{FAULT_RATIO}_error_kmeans'
else:
    EXP_NAME = f'solar_{CLIENT_NUMBER}_{FAULT_INDEX+1}_attack_{FAULT_RATIO}_error'

with open(os.path.join('.', 'detection.pkl'), 'rb') as f:
    data = pickle.load(f)
    
x_data = data['x_data']
y_data = data['y_data']
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1, random_state=42)
        

x_train, y_train = x_train[10000:], y_train[10000:]

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

try:
    os.makedirs(f"./logs/{EXP_NAME}")
except:
    pass

def generate_cmd(fault_index=FAULT_INDEX, model_type='cnn', exp_type='local', exp_name = EXP_NAME, client_num = CLIENT_NUMBER):

    if IS_KMEANS:
        cmds = [f'python client.py -c {i} -f {fault_index} -m {model_type} -e {exp_type} -n {exp_name} -k > ./logs/{exp_name}/client_{i}_fault_{fault_index}.log' for i in range(client_num)]
    else:
        cmds = [f'python client.py -c {i} -f {fault_index} -m {model_type} -e {exp_type} -n {exp_name} > ./logs/{exp_name}/client_{i}_fault_{fault_index}.log' for i in range(client_num)]
    print(' & '.join(cmds))
    return ' & '.join(cmds)


if len(x_train.shape) < 4:
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    

generate_dataset(x_train, y_train, x_test, y_test, CLIENT_NUMBER, FAULT_INDEX, falut_ratio=FAULT_RATIO)


os.system(f"nohup python server.py > ./logs/{EXP_NAME}/server.log 2>&1 &")

time.sleep(20)

os.system(generate_cmd())


# os.system("nohup python server.py > server.log 2>&1 &")

# "python client.py -c 0 -f -1 -m cnn -e local & python client.py -c 1 -f -1 -m cnn -e local"