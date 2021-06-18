import pickle
import os
from sklearn.model_selection import train_test_split
import numpy as np

def split_data(input_data, client_num, iid=True, abnormal_fraction = 0.75, workspace_dir='./', splited_data_folder='splited_data'):
    os.makedirs(os.path.join(workspace_dir, splited_data_folder))
    with open(os.path.join(workspace_dir, input_data), 'rb') as f:
        data = pickle.load(f)
    x_data = data['x_data']
    y_data = data['y_data']
    if not iid:
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1, random_state=42)
        with open(os.path.join(workspace_dir, splited_data_folder, f'test_data.pkl'), 'wb') as f:
            pickle.dump(dict(x_data=x_test, y_data=y_test), f)

        x_data_normal, x_data_abnormal = x_train[y_train==0], x_train[y_train==1]
        num_normal_client_0, num_abnormal_client_0 = int(len(x_data_normal) * (1-abnormal_fraction)), int(len(x_data_abnormal) * abnormal_fraction)
        num_normal_other, num_abnormal_other = (len(x_data_normal) - num_normal_client_0) // (client_num - 1), (len(x_data_abnormal) - num_abnormal_client_0) // (client_num - 1)
        
        for i in range(client_num):
            with open(os.path.join(workspace_dir, splited_data_folder, f'data_{i}.pkl'), 'wb') as f:
                if i == 0:
                    x_data = np.stack([x_data_abnormal[:num_abnormal_client_0], x_data_normal[:num_normal_client_0]])
                    y_data = np.vstack([np.zeros((num_abnormal_client_0,)), np.ones((num_normal_client_0,))])
                    pickle.dump(dict(x_data=x_data, y_data=y_data), f)

                    x_data_abnormal, x_data_normal = x_data_abnormal[num_abnormal_client_0:], x_data_normal[num_normal_client_0:]
                
                else:
                    
                    x_data = np.stack([x_data_abnormal[(i-1)*num_abnormal_other: i*num_abnormal_other], x_data_normal[(i-1)*num_normal_other: i*num_normal_other]])
                    y_data = np.vstack([np.zeros((num_abnormal_other,)), np.ones((num_normal_other,))])
                    pickle.dump(dict(x_data=x_data, y_data=y_data), f)

            print(f"split data {i}")
    else:
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1, random_state=42)
        with open(os.path.join(workspace_dir, splited_data_folder, f'test_data.pkl'), 'wb') as f:
            pickle.dump(dict(x_data=x_test, y_data=y_test), f)

        data_num = len(x_train) // client_num
        for i in range(client_num):
            with open(os.path.join(workspace_dir, splited_data_folder, f'data_{i}.pkl'), 'wb') as f:
                pickle.dump(dict(x_data=x_train[i*data_num: i*data_num+data_num], y_data=y_train[i*data_num:i*data_num+data_num]), f)
            print(f"split data {i}")
        
def clean_up_data(workspace_dir='./', splited_data_folder='splited_data'):
    if os.path.exists(os.path.join(os.path.join(workspace_dir, splited_data_folder))):
        for f in os.listdir(os.path.join(os.path.join(workspace_dir, splited_data_folder))):
            os.remove(os.path.join(workspace_dir, splited_data_folder, f))
        os.removedirs(os.path.join(workspace_dir, splited_data_folder))
