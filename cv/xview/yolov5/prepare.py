import json
import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm
from ultralytics.yolo.data.dataloaders.v5loader import autosplit
from ultralytics.yolo.utils.ops import xyxy2xywhn

# xView classes 11-94 to 0-59
xview_class2index = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, -1, 3, -1, 4, 5, 6, 7, 8, -1, 9, 10, 11,
                     12, 13, 14, 15, -1, -1, 16, 17, 18, 19, 20, 21, 22, -
                     1, 23, 24, 25, -1, 26, 27, -1, 28, -1,
                     29, 30, 31, 32, 33, 34, 35, 36, 37, -
                     1, 38, 39, 40, 41, 42, 43, 44, 45, -1, -1, -1, -1, 46,
                     47, 48, 49, -1, 50, 51, -1, 52, -1, -1, -1, 53, 54, -1, 55, -1, -1, 56, -1, 57, -1, 58, 59]


def load_geojson(fname):
    with open(fname) as f:
        print(f'Loading {fname}...')
        data = json.load(f)
    return data


def create_train_labels_dir(dataset_dir: Path):
    # create the labels directory
    train_labels_dir = Path(dataset_dir / 'labels' / 'train')
    # remove the directory content if it exists
    os.system(f'rm -rf {train_labels_dir}')
    # create the directory
    train_labels_dir.mkdir(parents=True, exist_ok=True)
    return train_labels_dir


def convert_labels(fname=Path('xView/xView_train.geojson')):
    """Convert xView geoJSON labels to YOLO format"""
    # Set fname to the path of the xView geoJSON file
    fname = Path(str(fname))
    # Set dataset_dir to the parent directory of the geoJSON file
    dataset_dir = fname.parent

    # Load the geoJSON file
    data = load_geojson(fname)
    # Create a directory to store the YOLO label files
    train_labels_dir = create_train_labels_dir(dataset_dir)

    # Create a dictionary to store the image sizes
    shapes = {}
    # Loop through each feature in the geoJSON file
    for feature in tqdm(data['features'], desc=f'Converting {fname}'):
        # Get xView label properties
        p = feature['properties']
        # Get image ID and file path
        id = p['image_id']
        file = dataset_dir / 'train_images' / id
        # Skip if image file does not exist
        if not file.exists():
            print(f'WARNING: skipping {file}')
            continue
        try:
            # Get bounding box coordinates
            box = np.array([int(num)
                           for num in p['bounds_imcoords'].split(",")])
            assert box.shape[0] == 4, f'incorrect box shape {box.shape[0]}'
            # Get xView class label
            cls = p['type_id']
            # Convert xView class label to 0-60 (number of classes)
            cls = xview_class2index[int(cls)]
            assert 59 >= cls >= 0, f'incorrect class index {cls}'
            # Write YOLO label
            if id not in shapes:
                shapes[id] = Image.open(file).size
            box = xyxy2xywhn(box[None].astype(np.float),
                             w=shapes[id][0], h=shapes[id][1], clip=True)
            with open((train_labels_dir / id).with_suffix('.txt'), 'a') as f:
                # write label.txt
                f.write(f"{cls} {' '.join(f'{x:.6f}' for x in box[0])}\n")
        except Exception as e:
            print(f'WARNING: skipping one label for {file}: {e}')


def unzip_dataset(dir: str):
    files = ['train_labels.zip',  # train labels
             'train_images.zip',  # 15G, 847 train images
             'val_images.zip']  # 5G, 282 val images (no labels)
    for file in files:
        os.system(f'unzip -n {dir / file} -d {dir}')


def move_images(dir: Path):
    # Create a directory to store the new image data
    images = Path(dir / 'images')
    images.mkdir(parents=True, exist_ok=True)

    # Move images
    train_images = dir / 'train_images'
    val_images = dir / 'val_images'
    # Move train images
    if train_images.exists():
        if (images / 'train').exists():
            shutil.rmtree(train_images)
        else:
            train_images.rename(dir / 'images' / 'train')
    # Move validation images
    if val_images.exists():
        if (images / 'val').exists():
            shutil.rmtree(val_images)
        else:
            val_images.rename(dir / 'images' / 'val')


def validate_yolo_structure(dir: Path):
    images = dir / 'images'
    assert (images / 'train').exists(), f'{images / "train"} does not exist'
    assert (images / 'val').exists(), f'{images / "val"} does not exist'
    assert (dir / 'labels' / 'train').exists(), f'{dir / "labels" / "train"} does not exist'
    assert (dir / 'labels' / 'val').exists(), f'{dir / "labels" / "val"} does not exist'


def xview_yolov5_prepare(dataset_dir: str = 'data/xView'):
    # Download manually from https://challenge.xviewdataset.org
    unzip_dataset(dataset_dir)
    convert_labels(dataset_dir / 'xView_train.geojson')
    move_images(dataset_dir)
    autosplit(dataset_dir / 'images' / 'train')
    validate_yolo_structure(dataset_dir)


if __name__ == '__main__':
    xview_yolov5_prepare()
