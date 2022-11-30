# humanoid-robot-pose

## Dataset Preparation

**Get video from camera**

```shell
python script/video_from_camera.py
```

**Convert video to image, to make the annotation part more general in any platform**

```shell
python script/get_image_from_video.py [name of folder that contains video]
```

**Split files inside folder to subfolder** <br>

```shell
python script/folder_splitter.py [name of folder] [number of files in seach subfolder folder]
```

If you are using ubuntu, you can check how many file inside folder, just type in terminal:

```shell
ls [name of folder] | wc -l
```
