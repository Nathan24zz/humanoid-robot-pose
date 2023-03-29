import os
import json
import numpy as np

path_to_fix_json = './val/'

def merge_json():
    json_files = [pos_json for pos_json in os.listdir(path_to_fix_json) if pos_json.endswith('.json')]
    first_time = True
    # check possible annotations for 1 image
    max_ann_each_image = 10
    # keep tracking current annotation index in list
    ann_idx = 0
    count_ann = 0

    # # make json file that is unorder (annotation part), appears first 
    # json_files.sort(key=lambda x: os.path.getmtime(f'train/{x}'), reverse=True)
    # loop every json files
    for file in json_files:
        if first_time: 
            # print(file)
            # exit()
            json_fisrt = json.load(open(f'{path_to_fix_json}{file}'))
            first_time = False
            json_fisrt['info']['description'] = 'Humanoid_robot_pose'
            # count_ann = json_fisrt['annotations'][-1]['id'] + 1
            count_ann = 2000
        else:
            data = json.load(open(f'{path_to_fix_json}{file}'))
            # get last image id in the first json
            last_id = json_fisrt['images'][-1]['id']

            for image in data['images']:
                current_img_id = image['id']
                # change id in images section
                image['id'] = last_id + 1
                # change image_id in annotations section
                for i in range(max_ann_each_image):
                    try:
                        if data['annotations'][ann_idx]['image_id'] == current_img_id:
                            # print(data['annotations'][ann_idx]['image_id'], current_img_id)
                            data['annotations'][ann_idx]['image_id'] = image['id']
                            data['annotations'][ann_idx]['id'] = count_ann
                            ann_idx += 1
                            # if i: print(f'{image["file_name"]} - id {image["id"]} has more than 1 annotation')
                        else:
                            # print(data['annotations'][ann_idx]['image_id'], current_img_id)
                            if not i: print(f'no annotations for image {image["file_name"]} - {data["info"]["description"]}')
                            break
                    except:
                        break
                    
                    count_ann += 1
                # make last_id equal to image['id'] for next iter
                last_id = image['id']
            ann_idx = 0

            # add images and annotations json to first json
            json_fisrt['images'] = json_fisrt['images'] + data['images']
            json_fisrt['annotations'] = json_fisrt['annotations'] + data['annotations']

    with open(f"{path_to_fix_json}merge.json", "w") as outfile:
        if not os.path.exists(path_to_fix_json):
            os.makedirs(path_to_fix_json)
        json_object = json.dumps(json_fisrt)
        outfile.write(json_object)

if __name__ == '__main__':
    merge_json()
