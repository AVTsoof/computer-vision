from typing import List, Tuple, Dict

XVIEW_CLASSES = ['Fixed-wing Aircraft', 'Small Aircraft', 'Cargo Plane', 'Helicopter', 'Passenger Vehicle', 'Small Car', 'Bus',
                 'Pickup Truck', 'Utility Truck', 'Truck', 'Cargo Truck', 'Truck w/Box', 'Truck Tractor', 'Trailer',
                 'Truck w/Flatbed', 'Truck w/Liquid', 'Crane Truck', 'Railway Vehicle', 'Passenger Car', 'Cargo Car',
                 'Flat Car', 'Tank car', 'Locomotive', 'Maritime Vessel', 'Motorboat', 'Sailboat', 'Tugboat', 'Barge',
                 'Fishing Vessel', 'Ferry', 'Yacht', 'Container Ship', 'Oil Tanker', 'Engineering Vehicle', 'Tower crane',
                 'Container Crane', 'Reach Stacker', 'Straddle Carrier', 'Mobile Crane', 'Dump Truck', 'Haul Truck',
                 'Scraper/Tractor', 'Front loader/Bulldozer', 'Excavator', 'Cement Mixer', 'Ground Grader', 'Hut/Tent', 'Shed',
                 'Building', 'Aircraft Hangar', 'Damaged Building', 'Facility', 'Construction Site', 'Vehicle Lot', 'Helipad',
                 'Storage Tank', 'Shipping container lot', 'Shipping Container', 'Pylon', 'Tower']
XVIEW_CLASSES_DICT_BY_NAME = {cls: i for i, cls in enumerate(XVIEW_CLASSES)}
XVIEW_CLASSES_DICT_BY_ID = {i: cls for i, cls in enumerate(XVIEW_CLASSES)}


def check_valid_classes(classes: List[str]):
    for cls in classes:
        if cls not in XVIEW_CLASSES:
            raise ValueError(f'Class {cls} is not a valid xView class')

def generate_classes_txt_file(output_labels_dir: str, classes: List[str], filename: str = 'classes.txt'):
    with open(str(output_labels_dir / filename), 'w') as f:
        for item in classes:
            f.write(item)
            # newline if not last item
            if item != classes[-1]:
                f.write('\n')