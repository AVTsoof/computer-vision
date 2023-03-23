from typing import List, Tuple, Dict
from pathlib import Path

from ..classes import *

def keep_classes(dir: Path, classes_to_keep: List[int]):
    """Keeps only the classes in classes_to_keep from the xView dataset in the directory dir"""
    # Iterate through each .txt file in the directory
    for file in dir.glob('*.txt'):
        # Open the file for reading
        with open(file, 'r') as f:
            # Read all lines in the file
            lines = f.readlines()
        # Open the file for writing
        with open(file, 'w') as f:
            # Iterate through each line in the file
            for line in lines:
                try:
                    # Split the line on spaces and take the first item
                    cls = line.split(' ')[0]
                    # If the class is in the list of classes to keep, write the line to the file
                    if cls in classes_to_keep:
                        f.write(line)
                except Exception as e:
                    print(f'Could not process line {line} with error {e}')
    print(f'Kept {len(classes_to_keep)} classes')


def get_classes_to_keep_from_txt(file: Path) -> List[str]:
    with open(file, 'r') as f:
        lines = f.readlines()
    classes_to_keep = [line.strip() for line in lines]
    return classes_to_keep


def xview_yolov5_keep_classes(dataset_dir: str, classes_to_keep_file: str):
    if not dataset_dir.exists():
        raise ValueError(f'Directory {dataset_dir} does not exist')
    if not classes_to_keep_file.exists():
        raise ValueError(f'File {classes_to_keep_file} does not exist')
    
    classes_to_keep = get_classes_to_keep_from_txt(classes_to_keep_file)
    check_valid_classes(classes_to_keep)
    keep_classes(dataset_dir, classes_to_keep)

