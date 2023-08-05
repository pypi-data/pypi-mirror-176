import json

from transform.augmentation.auto_orient import auto_orient
from transform.augmentation.resize_aug import ResizeAugmentation
from transform.augmentation.grayscale_aug import GrayscaleAugmentation
from transform.augmentation.contrast_equalization_aug import (
    ContrastEqualizationAugmentation,
)
from transform.augmentation.flip_aug import FlipAugmentation
from transform.augmentation.random_crop_aug import RandomCropAugmentation
from transform.augmentation.rotate_aug import RotateAugmentation
from transform.augmentation.select_annotation_aug import (
    SelectAnnotationAugmentation,
)
from transform.augmentation.shear_aug import ShearAugmentation
from transform.augmentation.brightness_aug import BrightnessAugmentation
from transform.augmentation.adjust_gamma_aug import AdjustGammaAugmentation
from transform.augmentation.blur_aug import BlurAugmentation
from transform.augmentation.noise_aug import NoiseAugmentation
from transform.augmentation.tile_aug import TileAugmentation
from transform.augmentation.mosaic_aug import MosaicAugmentation
from transform.augmentation.cutout_aug import CutoutAugmentation
from transform.augmentation.static_crop_aug import StaticCropAugmentation
from transform.augmentation.hue_aug import HueAugmentation
from transform.augmentation.saturation_aug import SaturationAugmentation

from transform.helper.polygon import annotation_points
from transform.helper.trim_annotations import trim_annotations

no_arg_augmentations = ("grayscale", "auto-orient")

# Act only on one image at a time
single_augmentations = {
    "resize": ResizeAugmentation,
    "grayscale": GrayscaleAugmentation,
    "auto-contrast": ContrastEqualizationAugmentation,
    "tile": TileAugmentation,
    "flip": FlipAugmentation,
    "crop": RandomCropAugmentation,
    "ninety": RotateAugmentation,
    "rotate": RotateAugmentation,
    "shear": ShearAugmentation,
    "brightness": BrightnessAugmentation,
    "exposure": AdjustGammaAugmentation,
    "blur": BlurAugmentation,
    "noise": NoiseAugmentation,
    "cutout": CutoutAugmentation,
    "static-crop": StaticCropAugmentation,
    "hue": HueAugmentation,
    "saturation": SaturationAugmentation,
    "select-annotation": SelectAnnotationAugmentation,
}

# Act on multiple images at a time
multi_augmentations = {"mosaic": MosaicAugmentation}


def process_labeled_image(command, args, image, annotation, mask, img_path):
    if command == "auto-orient":
        return auto_orient(
            img=image, annotation=annotation, mask=mask, img_path=img_path
        )
    elif command in single_augmentations:
        return single_augmentations[command](
            image, annotation, mask, args
        ).call()


class ProcessingCommand:
    def __init__(self, step, images, annotations, masks, img_path):
        self.parts = step.split(":", 1)

        self.command = self.parts[0]

        if (
            (len(self.parts) > 1)
            and self.parts[1] != ""
            and self.parts[1][0] == "["
        ):
            self.args = json.loads(self.parts[1])
        else:
            self.args = None

        self.step = step
        self.images = images
        self.annotations = annotations
        self.masks = masks
        self.img_path = img_path

    def empty(self):
        return len(self.parts) <= 1 or (
            len(self.parts) > 1 and self.parts[1] == ""
        )


# Convert annotation coordinates to floats
def parse_annotations(annotations):
    for annotation_list in annotations:
        if "width" in annotation_list:
            annotation_list["width"] = float(annotation_list["width"])
        if "height" in annotation_list:
            annotation_list["height"] = float(annotation_list["height"])
        for annotation in annotation_list.get("boxes", []):
            if annotation is not None:
                x = annotation.get("x", None)
                y = annotation.get("y", None)
                width = annotation.get("width", None)
                height = annotation.get("height", None)

                if (
                    (x is None)
                    or (y is None)
                    or (width is None)
                    or (height is None)
                ):
                    print("Image missing x, y, width, or height annotations")
                    continue

                annotation["x"] = float(annotation["x"])
                annotation["y"] = float(annotation["y"])
                annotation["width"] = float(annotation["width"])
                annotation["height"] = float(annotation["height"])

                points = annotation_points(annotation)
                if points:
                    annotation["points"] = [
                        [float(coordinate) for coordinate in point]
                        for point in points
                    ]
            else:
                print(
                    "WARNING: Annotation is None in process.parse_annotation"
                )
    return annotations


def process(step, images, annotations, masks, img_path):
    """
    Image level comands should be in the form `command:[arg1, arg2, ...]`

    Bounding box level commands should be in the form
    `command:[[arg1, arg2, ...], ...]` with one array for each bounding box
    """
    if not annotations:
        raise TypeError(
            "Annotations cannot be of type None (can be a list of type None)!"
        )
    if len(images) != len(annotations):
        raise ValueError(
            "Each image must have a corresponding annotation (can be 'None', but list length must match)"
        )

    pcommand = ProcessingCommand(step, images, annotations, masks, img_path)

    # Ignores commands without arguments unless they're in the whitelist
    # E.g., "flip:" is not allowed but "grayscale" is
    if pcommand.empty() and step not in no_arg_augmentations:
        return images, annotations, masks

    annotations = parse_annotations(annotations)

    command = pcommand.command
    args = pcommand.args
    if command in single_augmentations or command == "auto-orient":
        labeled_images = list(zip(images, annotations, masks))
        augmented_labeled_images = [
            process_labeled_image(
                command, args, image, annotation, mask, img_path
            )
            for image, annotation, mask in labeled_images
        ]
        keep = 20
        if command == "tile":
            keep = 0
        trimmed_labeled_images = [
            trim_annotations(image, annotation, mask, keep=keep)
            for image, annotation, mask in augmented_labeled_images
        ]
        processed_labeled_images = list(zip(*trimmed_labeled_images))
    elif command in multi_augmentations:
        return multi_augmentations[command](
            images, annotations, masks, args
        ).call()
    elif command == "remap":
        # skip
        return images, annotations, masks
    else:
        print("command not yet implemented: " + command)
        return images, annotations, masks

    return processed_labeled_images
