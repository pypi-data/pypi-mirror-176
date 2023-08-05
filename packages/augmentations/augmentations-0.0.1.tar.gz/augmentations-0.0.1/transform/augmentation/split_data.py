import copy
import glob
import os
import xml.etree.ElementTree as ET
import shutil
import argparse

from PIL import Image
from skimage.io import imread as imread
import numpy as np


def bound(annotation, img):
    """
    Deals with annotations, including those that have bounds beyond the image:
     - Returns cropped bounds for those beyond the image
     - Returns original bounds for those not beyond the image
    :param annotation: <xml.etree.ElementTree.Element>
    :param img: <np.ndarray>
    :return: <tuple> (min_x, max_x, min_y, max_y)
    """

    input_width = img.shape[1]
    input_height = img.shape[0]

    bndbox = annotation.find("bndbox")
    min_x = int(bndbox.find("xmin").text)
    max_x = int(bndbox.find("xmax").text)
    min_y = int(bndbox.find("ymin").text)
    max_y = int(bndbox.find("ymax").text)

    if (
        (min_x < 0)
        or (min_y < 0)
        or (max_x >= input_width)
        or (max_y >= input_height)
    ):

        if (
            (min_x > input_width - 1)
            or (min_y > input_height - 1)
            or (max_x < 0)
            or (max_y < 0)
        ):
            # entirely out of frame
            return

        min_x = max(min_x, 0)
        min_y = max(min_y, 0)
        max_x = min(max_x, input_width - 1)
        max_y = min(max_y, input_height - 1)

        if (max_x < min_x) or (max_y < min_y):
            print(f"min_x: {min_x}")
            print(f"max_x: {max_x}")
            print(f"min_y: {min_y}")
            print(f"max_y: {max_y}")
            raise Exception(
                "max_x is less than min_x or max_y is less than min_y"
            )
    return (min_x, max_x, min_y, max_y)


def handle_piece(
    image, annotations_tree, shift_x, shift_y, new_width, new_height, keep
):
    annotations = annotations_tree.getroot()
    size = annotations.find("size")
    size.find("width").text = str(new_width)
    size.find("height").text = str(new_height)

    annotations_to_remove = []

    for annotation in annotations.findall("object"):

        bndbox = annotation.find("bndbox")

        bndbox.find("xmin").text = str(int(bndbox.find("xmin").text) - shift_x)
        bndbox.find("xmax").text = str(int(bndbox.find("xmax").text) - shift_x)
        bndbox.find("ymin").text = str(int(bndbox.find("ymin").text) - shift_y)
        bndbox.find("ymax").text = str(int(bndbox.find("ymax").text) - shift_y)

        bounds = bound(annotation, image)
        if not bounds:
            annotations_to_remove.append(annotation)
            continue

        (min_x, max_x, min_y, max_y) = bounds
        area_in_bounds = (max_x - min_x) * (max_y - min_y)
        image_width = int(annotations.find("size").find("width").text)
        image_height = int(annotations.find("size").find("height").text)
        total_area = image_width * image_height

        if total_area <= 0:
            print(
                "handle_piece: annotation area", total_area, "is not positive!"
            )
            continue

        if area_in_bounds / total_area >= keep:
            bndbox = annotation.find("bndbox")
            bndbox.find("xmin").text = str(min_x)
            bndbox.find("xmax").text = str(max_x)
            bndbox.find("ymin").text = str(min_y)
            bndbox.find("ymax").text = str(max_y)
        else:
            annotations_to_remove.append(annotation)

    for annotation in annotations_to_remove:
        annotations.remove(annotation)

    return image, annotations_tree


def split_data(image, annotations_tree, count=(2, 2), keep=0):
    """
    :param image: <np.ndarray>
    :param annotations_tree: <xml.etree.ElementTree>
    :param count: <tuple<int, int>> (x_piece_count, y_piece_count)
    :param keep: <float>
    """

    annotations = annotations_tree.getroot()

    width = int(annotations.find("size").find("width").text)
    height = int(annotations.find("size").find("height").text)

    new_width = int(width / count[0])
    new_height = int(height / count[1])

    pieces = []
    # Appends in correct order
    for j in range(count[1]):
        for i in range(count[0]):
            height_range = np.s_[j * new_height : (j + 1) * new_height]
            width_range = np.s_[i * new_width : (i + 1) * new_width]
            annotations_tree_copy = copy.deepcopy(annotations_tree)
            root = annotations_tree_copy.getroot()
            root.find("filename").text = (
                root.find("filename").text[:-4]
                + "_"
                + str(i + j * count[0] + 1)
                + ".jpg"
            )
            root.find("path").text = (
                root.find("path").text[:-4]
                + "_"
                + str(i + j * count[0] + 1)
                + ".jpg"
            )
            # p_ for Partial
            piece = handle_piece(
                image[height_range, width_range],
                annotations_tree_copy,
                i * new_width,
                j * new_height,
                new_width,
                new_height,
                keep,
            )
            pieces.append(piece)
    return pieces


def read_image(path):
    return imread(path + ".jpg").astype(np.float64) / 255


def read_annotations(path):
    tree = ET.parse(path + ".xml")

    return tree


def read_data(path):
    image = read_image(path)
    annotations = read_annotations(path)

    return image, annotations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split images and update annotations accordingly. Annotations must be in Pascal VOC format. Output will be in a directory with suffix `-split`."
    )
    parser.add_argument(
        "input_path",
        help="Path to directory. Should contain train/valid/test subdirectories, each of which contain images and annotations.",
    )
    parser.add_argument(
        "--keep",
        help="For bounding boxes that are parially in-frame. Bounding boxes with in-frame area below this threshold (as a percent of their area) are dropped. Default zero.",
    )
    args = parser.parse_args()

    input_path = args.input_path
    keep = args.keep or 0
    keep = int(keep)

    (input_path, dataset_name) = os.path.split(input_path)
    if not dataset_name:
        dataset_name = os.path.split(input_path)[-1]
        (input_path, dataset_name) = os.path.split(input_path)
    dataset_output_name = dataset_name + "-split"

    dirs = ["train", "test", "valid"]

    os.chdir(input_path)
    star_paths = [os.path.join(dataset_name, dir) + "/*.jpg" for dir in dirs]
    tree_paths = list(
        map(glob.glob, star_paths)
    )  # [os.path.join(input_path, star_path) for star_path in star_paths]
    paths = [item for sublist in tree_paths for item in sublist]

    def mkdir_safe(dir):
        if os.path.isdir(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)

    mkdir_safe(dataset_output_name)
    for dir in dirs:
        mkdir_safe(os.path.join(dataset_output_name, dir))

    for path in paths:
        data = read_data(path[:-4])  # omit .jpg extension
        pieces = split_data(*data, keep=keep)
        new_path = path.replace(dataset_name, dataset_output_name)[:-4]
        for (i, piece) in enumerate(pieces):
            image = piece[0]
            image *= 255
            image = image.astype(np.uint8)
            img = Image.fromarray(image)
            if img.mode == "RGBA":
                img = img.convert("RGB")

            new_path_pieced = new_path + "_" + str(i + 1)

            img.save(new_path_pieced + ".jpg")

            annotations_tree = piece[1]
            annotations_tree.write(
                new_path_pieced + ".xml", short_empty_elements=False
            )
