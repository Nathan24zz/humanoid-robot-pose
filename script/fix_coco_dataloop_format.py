import os
import json
import numpy as np

path_to_json = './json_dataloop/'
path_to_fix_json = './json_dataloop_fix/'

def fix_dataloop_format():
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    num_keypoints = 0
    
    # loop every json files
    for file in json_files:
        data = json.load(open(f'{path_to_json}{file}'))
        # FIX CATEGORIES
        new_categories = []
        for category in data['categories']:
            try:
                if category['skeleton'] is not None: 
                    new_categories.append(category)
                    new_categories[0]['id'] = 1
                    new_categories[0]['supercategory'] = new_categories[0]['name']
                    del new_categories[0]['templateId']
                    num_keypoints = len(new_categories[0]['keypoints'])

                    # # format for nimbro training
                    # # add 1 in every value in skeleton
                    # new_categories[0]['skeleton'] = np.array(new_categories[0]['skeleton'])
                    # new_categories[0]['skeleton'] += 1
                    # # make it back to list
                    # new_categories[0]['skeleton'] = new_categories[0]['skeleton'].tolist()

                    # replace categories with new categories
                    data['categories'] = new_categories
            except:
                pass
        
        # FIX ANNOTATIONS
        new_annotations = []
        if len(data['annotations']) > 0:
            for annotation in data['annotations']:
                annotation['segmentation'] = []
                annotation['num_keypoints'] = num_keypoints
                annotation['category_id'] = 1

                # change keypoints (x,y,v,....) visibility to 1
                index = 1
                new_list = []
                for value in annotation['keypoints']:
                    if index == 3: 
                        new_list.append(1)
                        index = 1
                    else:
                        new_list.append(value)
                        index += 1
                annotation['keypoints'] = new_list
                new_annotations.append(annotation)

            # replace annotations with new annotations
            data['annotations'] = new_annotations
        else:
            print('annotations is null')

        # save json
        if not os.path.exists(path_to_fix_json):
            os.makedirs(path_to_fix_json)
        with open(f"{path_to_fix_json}{file}", "w") as outfile:
            json_object = json.dumps(data)
            outfile.write(json_object)

def merge_json():
    json_files = [pos_json for pos_json in os.listdir(path_to_fix_json) if pos_json.endswith('.json')]
    first_time = True
    # check possible annotations for 1 image
    max_ann_each_image = 10
    # keep tracking current annotation index in list
    ann_idx = 0
    count_ann = 0

    # loop every json files
    for file in json_files:
        if first_time: 
            json_fisrt = json.load(open(f'{path_to_fix_json}{file}'))
            first_time = False
            json_fisrt['info']['description'] = 'Humanoid_robot_pose'
            count_ann = json_fisrt['annotations'][-1]['id'] + 1
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
    fix_dataloop_format()
    merge_json()