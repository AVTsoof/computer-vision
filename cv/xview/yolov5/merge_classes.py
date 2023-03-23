import argparse
import json
from typing import List, Tuple, Dict
from pathlib import Path

import fire

from ..classes import *


def check_args(args):
    if not args.input_labels_dir.exists():
        raise ValueError(f'Directory {args.input_labels_dir} does not exist')
    if not args.classes_to_merge_file.exists():
        raise ValueError(f'File {args.classes_to_merge_file} does not exist')


def validate_classes_to_merge(classes_to_merge: Dict[str, List[str]]):
    """Validate that the classes to merge are valid
    
    Args:
        classes_to_merge (dict): A dictionary containing the classes to merge.
            The keys are the classes to merge into, and the value is a list of 
            classes to merge. For example: {'building': ['commercial', 'residential']}
    
    Raises:
        ValueError: If any of the classes to merge are not valid xView classes
    """
    for key, value in classes_to_merge.items():
        for cls in value:
            if cls not in XVIEW_CLASSES:
                raise ValueError(f'Class {cls} is not a valid xView class')


def get_classes_to_merge_from_file(jsonfile: Path) -> Dict[str, List[str]]:
    with open(jsonfile, 'r') as f:
        classes_to_merge = json.load(f)
    validate_classes_to_merge(classes_to_merge)
    return classes_to_merge

def write_list_to_txt_file(file: Path, lst: List[str]):
    with open(str(file), 'w') as f:
        for item in lst:
            f.write(item)
            # newline if not last item
            if item != lst[-1]:
                f.write('\n')

def get_classes_to_merge_ids(classes_to_merge: Dict[str, List[str]]) -> Dict[int, List[int]]:
    classes_to_merge_ids = {}
    for key, value in classes_to_merge.items():
        classes_to_merge_ids[XVIEW_CLASSES.index(key)] = [XVIEW_CLASSES.index(cls) for cls in value]
    return classes_to_merge_ids

def merge_classes(input_labels_dir: Path, output_labels_dir: Path, classes_to_merge_ids: Dict[int, List[int]]):
    for file in input_labels_dir.iterdir():
        if file.suffix == '.txt':
            with open(file, 'r') as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                line = line.strip()
                line = line.split(' ')
                cls_id = int(line[0])
                if cls_id in classes_to_merge_ids:
                    for cls in classes_to_merge_ids[cls_id]:
                        new_line = line.copy()
                        new_line[0] = str(cls)
                        new_line = ' '.join(new_line)
                        new_lines.append(new_line)
                else:
                    new_lines.append(' '.join(line))
            with open(output_labels_dir / file.name, 'w') as f:
                for line in new_lines:
                    f.write(line)
                    # newline if not last item
                    if line != new_lines[-1]:
                        f.write('\n')

def xview_yolov5_merge_classes(input_labels_dir: Path, output_labels_dir: Path, classes_to_merge_file: Path):
    if not input_labels_dir.exists():
        raise ValueError(f'Directory {input_labels_dir} does not exist')
    if not classes_to_merge_file.exists():
        raise ValueError(f'File {classes_to_merge_file} does not exist')

    Path(output_labels_dir).mkdir(parents=True, exist_ok=True)
    
    classes_to_merge = get_classes_to_merge_from_file(classes_to_merge_file)
    generate_classes_txt_file(output_labels_dir, classes_to_merge.keys())
    classes_to_merge_ids = get_classes_to_merge_ids(classes_to_merge)
    
    merge_classes(input_labels_dir, output_labels_dir, classes_to_merge_ids)


