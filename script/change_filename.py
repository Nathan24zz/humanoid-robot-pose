import os
import json
import numpy as np

json_name = './train_kidsize/ichiro_new.json'
path_to_img = './dataset_images/'
name_start_img = 'output100_'
path_to_fix_json = './train_kidsize/'

def change_file_name():
    data = json.load(open(json_name))

    count_idx_img = 0 
    for idx in range(len(data['images'])):
        source = data['images'][idx]['file_name']
        data['images'][idx]['file_name'] = name_start_img + str(count_idx_img) + '.jpg'
        count_idx_img += 1
        destination = data['images'][idx]['file_name']
        # change image name
        os.rename(path_to_img + source, path_to_img + destination)

    with open(json_name, "w") as outfile:
        json_object = json.dumps(data)
        outfile.write(json_object)

if __name__ == '__main__':
    change_file_name()
