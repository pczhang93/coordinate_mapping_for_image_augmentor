# coordinate_mapping_for_image_augmentor
The script is aim to generate corresponding annotation files in VIA format for new generated images after data augmentation by [image_augmentor](https://github.com/codebox/image_augmentor).

Before run the script, you need to put the augmented images([image_augmentor](https://github.com/codebox/image_augmentor)) folder and the VIA([VGG Image Annotator](http://www.robots.ox.ac.uk/~vgg/software/via/via.html)) format JSON file that annotate the original images in the current directory.And add the two parameters of [images_folder_name] and [json_name],when running the script.

```
python coordinate_mapping.py [images_folder_name] [json_name]
```
