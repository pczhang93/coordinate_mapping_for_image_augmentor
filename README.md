# coordinate_mapping_for_image_augmentor
#### The script is aim to generate corresponding annotation files(Maybe it is to augment data sets for training instance segmentation models) in VIA（[VGG Image Annotator](http://www.robots.ox.ac.uk/~vgg/software/via/via.html)） format for new generated images after data augmentation by [image_augmentor](https://github.com/codebox/image_augmentor).

#### Before run the script, you need to put the augmented images folder and the VIA format JSON file that annotate the original images in the current directory. And add the two parameters of [images_folder_name] and [json_name], when running the script.
```
python coordinate_mapping.py [images_folder_name] [json_name]
```
 
#### The script will parse its corresponding data augmentation method by image name and transform coordinates to generate new annotation file.

#### After the script is run, the newly generated JSON file will be named after [images_folder_name].

####The current version is to discard the point directly beyond the image boundary after transformation.


