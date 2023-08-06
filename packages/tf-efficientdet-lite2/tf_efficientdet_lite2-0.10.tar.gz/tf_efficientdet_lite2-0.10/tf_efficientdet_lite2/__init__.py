import os
import random
from pathlib import Path
from typing import Any, Union

import pandas as pd
import regex
import requests
import tensorflow_hub
from appdirs import user_cache_dir
from subprocess_pipe import pipe_commands
import cv2
import tensorflow as tf
from a_cv_imwrite_imread_plus import open_image_in_cv


all_labels = {
    1: "person",
    2: "bicycle",
    3: "car",
    4: "motorcycle",
    5: "airplane",
    6: "bus",
    7: "train",
    8: "truck",
    9: "boat",
    10: "traffic light",
    11: "fire hydrant",
    12: "street sign",
    13: "stop sign",
    14: "parking meter",
    15: "bench",
    16: "bird",
    17: "cat",
    18: "dog",
    19: "horse",
    20: "sheep",
    21: "cow",
    22: "elephant",
    23: "bear",
    24: "zebra",
    25: "giraffe",
    26: "hat",
    27: "backpack",
    28: "umbrella",
    29: "shoe",
    30: "eye glasses",
    31: "handbag",
    32: "tie",
    33: "suitcase",
    34: "frisbee",
    35: "skis",
    36: "snowboard",
    37: "sports ball",
    38: "kite",
    39: "baseball bat",
    40: "baseball glove",
    41: "skateboard",
    42: "surfboard",
    43: "tennis racket",
    44: "bottle",
    45: "plate",
    46: "wine glass",
    47: "cup",
    48: "fork",
    49: "knife",
    50: "spoon",
    51: "bowl",
    52: "banana",
    53: "apple",
    54: "sandwich",
    55: "orange",
    56: "broccoli",
    57: "carrot",
    58: "hot dog",
    59: "pizza",
    60: "donut",
    61: "cake",
    62: "chair",
    63: "couch",
    64: "potted plant",
    65: "bed",
    66: "mirror",
    67: "dining table",
    68: "window",
    69: "desk",
    70: "toilet",
    71: "door",
    72: "tv",
    73: "laptop",
    74: "mouse",
    75: "remote",
    76: "keyboard",
    77: "cell phone",
    78: "microwave",
    79: "oven",
    80: "toaster",
    81: "sink",
    82: "refrigerator",
    83: "blender",
    84: "book",
    85: "clock",
    86: "vase",
    87: "scissors",
    88: "teddy bear",
    89: "hair drier",
    90: "toothbrush",
    91: "hair brush",
}


def download_tensorflow_tohdd_and_load(
    tensorflowlink, sevenzip_path=r"C:\Program Files\7-Zip\7z.exe", force_download=False
):
    tensorflowpath = regex.sub(r"\W+", "_", tensorflowlink) + ".tar.gz"
    CACHE_DIR = Path(user_cache_dir("tensorflowmodels"))
    modeldir = os.path.join(CACHE_DIR, regex.sub(r"\W+", "_", tensorflowlink))
    tensorflowpathhdd = os.path.join(CACHE_DIR, tensorflowpath)
    if force_download:
        try:
            os.remove(tensorflowpathhdd)
        except Exception:
            pass
    else:
        if os.path.exists(modeldir):
            try:
                return tensorflow_hub.load(modeldir)
            except Exception:
                pass

    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir(parents=True)
    if not os.path.exists(tensorflowpathhdd):
        tenslink = requests.get(tensorflowlink).content
        with open(tensorflowpathhdd, mode="wb") as f:
            f.write(tenslink)
    pipe_commands(
        [sevenzip_path, "x", tensorflowpathhdd, "-so"],
        [sevenzip_path, "x", "-aoa", "-si", "-ttar", f"-o{modeldir}"],
    )
    return tensorflow_hub.load(modeldir)


def load_model(
    modelurl="https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1",
    sevenzip_path=r"C:\Program Files\7-Zip\7z.exe",
):
    if os.path.exists(str(sevenzip_path)):
        try:
            detector = download_tensorflow_tohdd_and_load(
                modelurl, sevenzip_path=sevenzip_path, force_download=False
            )
        except Exception:
            detector = tensorflow_hub.load(modelurl)

    else:
        detector = tensorflow_hub.load(modelurl)
    return detector


def get_person_coords(
    image, detector=None, draw_results=True, draw_result_min_score=0.5
):
    frame = open_image_in_cv(image, channels_in_output=3, bgr_to_rgb=False).copy()
    rgb = frame.copy()
    rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)
    rgb_tensor = tf.expand_dims(rgb_tensor, 0)
    boxes, scores, classes, num_detections = detector(rgb_tensor)
    pred_labels = classes.numpy()[0].astype("int")
    pred_boxes = boxes.numpy()[0].astype("int")
    pred_scores = scores.numpy()[0]
    if draw_results:

        for score, (ymin, xmin, ymax, xmax), label in zip(
            pred_scores, pred_boxes, pred_labels
        ):
            r_g_b_ = (
                random.randrange(50, 255),
                random.randrange(50, 255),
                random.randrange(50, 255),
            )
            if score < draw_result_min_score:
                continue
            rgb = cv2.rectangle(rgb, (xmin, ymax), (xmax, ymin), (0, 0, 0), 3)

            rgb = cv2.rectangle(rgb, (xmin, ymax), (xmax, ymin), r_g_b_, 2)

            rgb = cv2.putText(
                rgb,
                str(all_labels.get(label)),
                (xmin, ymax),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 0),
                3,
            )
            rgb = cv2.putText(
                rgb,
                str(all_labels.get(label)),
                (xmin, ymax),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                r_g_b_,
                2,
            )
    df1 = pd.DataFrame(classes.numpy().astype("int")[0])
    df1.columns = ["aa_class"]
    df2 = pd.DataFrame(boxes.numpy().astype("int")[0])
    df2.columns = ["aa_x_start", "aa_y_start", "aa_x_end", "aa_y_end"]
    df3 = pd.DataFrame(scores.numpy().astype("float")[0])
    df3.columns = ["aa_conf"]
    df = pd.concat([df1, df2, df3], axis=1)
    df.aa_class = df.aa_class.map(lambda x: all_labels.get(x))
    return df, rgb


def cv2resize(image, dim, interpolation=cv2.INTER_AREA):
    return cv2.resize(image.copy(), dim, interpolation=interpolation)

def cv2_resize_fixed_width(img, width=100):
    dim = get_new_relative_size_from_width(img, width=width)
    bia1 = cv2resize(img, dim)
    return bia1

def get_new_relative_size_from_width(img, width=100):
    ratio = img.shape[0] / img.shape[1]
    height = width * ratio
    dim = (int(width), int(height))
    return dim

class TfEfficientdetLite2:
    def __init__(
        self,
        sevenzip_path: Union[str, None] = r"C:\Program Files\7-Zip\7z.exe",
        set_visible_devices_0: bool = True,
    ):
        if set_visible_devices_0:
            tf.config.experimental.set_visible_devices([], "GPU")

        self.detector = load_model(
            modelurl="https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1?tf-hub-format=compressed",
            sevenzip_path=sevenzip_path,
        )
        self.df = pd.DataFrame()
        self.drawn_results = None

    def detect(
        self, image: Any, draw_results: bool = False, draw_result_min_score: float = 0.3,
    resize_width=800):

        image = open_image_in_cv(image)
        image=cv2_resize_fixed_width(image, width=resize_width)
        self.df, self.drawn_results = get_person_coords(
            image,
            detector=self.detector,
            draw_results=draw_results,
            draw_result_min_score=draw_result_min_score,
        )
        return self

    def get_df(self):
        return self.df.copy()

    def get_drawn_results(self):
        return self.drawn_results.copy()
