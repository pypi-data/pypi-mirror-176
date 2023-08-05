from PIL import Image
import piexif
import numpy as np


# https://piexif.readthedocs.io/en/latest/sample.html
# NOTE: this presumes an image is read with PIL and a JPEG to contain correct EXIF data!
def auto_orient(img, annotation, mask, img_path):
    orig = img
    # hack to read in IMG in PIL for this function only
    img_path = img_path
    img = Image.open(img_path).convert("RGB")
    info = img.info
    # print("GETTING INFO:  ", info)

    if "exif" in info:

        try:
            exif_dict = piexif.load(info["exif"])
            print("FOUND EXIF")
            if piexif.ImageIFD.Orientation in exif_dict["0th"]:

                print("FOUND ORIENTATION")

                orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                # exif_bytes = piexif.dump(exif_dict)

                if orientation == 2:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    img = img.rotate(180)
                elif orientation == 4:
                    img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 5:
                    img = img.rotate(-90, expand=True).transpose(
                        Image.FLIP_LEFT_RIGHT
                    )
                elif orientation == 6:
                    img = img.rotate(-90, expand=True)
                elif orientation == 7:
                    img = img.rotate(90, expand=True).transpose(
                        Image.FLIP_LEFT_RIGHT
                    )
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

                # convert to numpy array
                img_np = np.array(img).astype(np.float64) / 255

                return img_np, annotation, mask
        except Exception:
            print("HAD AN EXIF ERROR ON THIS IMG")
            pass

    # else return original
    return orig, annotation, mask
