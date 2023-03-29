import os
import json
import numpy as np

path_to_json = './json/'
path_to_fix_json = './json_fix/'

def fix_coco_annotator_format():
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    # print(json_files)
    # loop every json files
    for file in json_files:
        data = json.load(open(f'{path_to_json}{file}'))
        # FIX INFO
        data['info'] = {'description': 'HumanoidRobotPose Dataset'}
        
        # FIX IMAGES
        new_images = []
        new_image = {}
        # print(data['images'][0])
        # exit()
        for image in data['images']:
            new_image['file_name'] = image['file_name']
            new_image['height'] = image['height']
            new_image['width'] = image['width']
            new_image['id'] = image['id']
            new_images.append(new_image)
            new_image = {}
        # print(new_image)
        # print(image)
        # exit()
        # replace image with new image
        data['images'] = new_images
        
        # FIX CATEGORIES
        new_category = {}
        for category in data['categories']:
            try:
                if category['skeleton'] is not None: 
                    new_category['name'] = 'robot'
                    new_category['supercategory'] = 'robot'
                    new_category['skeleton'] = category['skeleton']
                    new_category['keypoints'] = category['keypoints']
                    new_category['id'] = 1

                    data['categories'] = [new_category]
            except:
                pass

        # FIX ANNOTATIONS
        new_annotations = []
        new_annotation = {}
        if len(data['annotations']) > 0:
            for annotation in data['annotations']:
                new_annotation['segmentation'] = []
                new_annotation['num_keypoints'] = annotation['num_keypoints']
                new_annotation['category_id'] = 1
                new_annotation['iscrowd'] = 0
                
                # change keypoints (x,y,v,....) visibility to 1
                x = {'min': None, 'max': None}
                y = {'min': None, 'max': None}
                new_list = []
                for index, value in enumerate(annotation['keypoints']):
                    if index % 3 == 2 and value != 0: 
                        new_list.append(1)
                    else:
                        if index % 3 == 0 and value != 0:
                            if x['min'] == None or value < x['min']: x['min'] = value
                            if x['max'] == None or value > x['max']: x['max'] = value
                        elif index % 3 == 1 and value != 0:
                            if y['min'] == None or value < y['min']: y['min'] = value
                            if y['max'] == None or value > y['max']: y['max'] = value
                        new_list.append(value)
                new_annotation['keypoints'] = new_list
                
                new_annotation['image_id'] = annotation['image_id']
                new_annotation['bbox'] = [x['min'], y['min'], x['max'] - x['min'], y['max'] - y['min']]
                new_annotation['area'] = new_annotation['bbox'][2] * new_annotation['bbox'][3]
                new_annotation['category_id'] = 1
                new_annotation['id'] = annotation['id']
                
                new_annotations.append(new_annotation)
                new_annotation = {}
                
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

if __name__ == '__main__':
    fix_coco_annotator_format()