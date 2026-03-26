import os
import folder_paths
import numpy as np

from PIL import Image, ImageOps

import torch
import node_helpers

class AnyType(str):
    def __eq__(self, _) -> bool:
        return True

    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

class Rload:
    @classmethod
    def INPUT_TYPES(s):
        # input_dir = folder_paths.get_input_directory()
        # files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.endswith(".npy")]
        # return {"required": {"npy": [sorted(files), ]}, }
        return {
            "required": {
                "file_path": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": "ComfyUI_00001_"})
            }
        }

    RETURN_TYPES = (any, )
    RETURN_NAMES = ("output", )
    FUNCTION = "load"
    CATEGORY = "ResourcesSL"

    # def load(self, npy, anything=None):
        # npy_path = folder_paths.get_annotated_filepath(npy)
    def load(self, file_path="", file_name="ComfyUI_00001_", anything=None):
        filename_prefix = file_path + file_name
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix,
            folder_paths.get_output_directory()
        )
        file = f"{filename}.npy"
        npy_path = os.path.join(full_output_folder, file)

        npyg = np.load(npy_path, allow_pickle=True)
        # print(f"{npyg}")
        try:
            anything = torch.from_numpy(npyg[0])[None,]
        except Exception as e:
            anything = npyg
            # print(f"{e}")
        # print(f"{anything}")
        return (anything, )

class RloadImageC:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "anything": (any, {})
            }
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("images", )
    FUNCTION = "imagecl"
    CATEGORY = "ResourcesSL"

    def imagecl(self, anything=None):
        imageg = []
        for imgb in anything:
            img = Image.open(imgb)
            img = node_helpers.pillow(ImageOps.exif_transpose, img)
            # print(f"{img.mode}")
            if img.mode == 'I':
                img = img.point(lambda img: img * (1 / 255))
            imgd = img.convert("RGB")
            i = np.array(imgd).astype(np.float32) / 255.0
            im = torch.from_numpy(i)[None,]
            imageg.append(im)
        if len(imageg) > 1:
            output_image = torch.cat(imageg, dim=0)
        else:
            output_image = imageg[0]
        return (output_image, )

NODE_CLASS_MAPPINGS = {
    "Rload": Rload,
    "RloadImageC": RloadImageC,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Rload": "Rload",
    "RloadImageC": "RloadImageC",
}
