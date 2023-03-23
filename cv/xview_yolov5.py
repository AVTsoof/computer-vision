import fire

from .xview.yolov5 import *

if __name__ == '__main__':
    fire.Fire(dict(
        prepare=xview_yolov5_prepare,
        keep_classes=xview_yolov5_keep_classes,
        merge_classes=xview_yolov5_merge_classes,
    ))