import os

from PIL import Image,ImageDraw
from copy_util import *

### shrink and copy images

def shrink_by_width(src_img):
    im = src_img.convert('RGB')
    w_o, h_o = im.size
    plMode = 0 if w_o > h_o else 1
    whl = {"w": w_o, "h": h_o}
    if plMode == 1:
        wh = ["w", "h"]

    if plMode == 0:
        resizeScale = width_limit / whl["w"]
        resizeFile = {
            "w": width_limit,
            "h": int(whl["h"] * resizeScale)
        }
    else:
        resizeScale = width_limit / whl["h"]
        resizeFile = {
            "h": width_limit,
            "w": int(whl["w"] * resizeScale)
        }
    return im.resize((resizeFile["w"], resizeFile["h"]))

def shrink_image_size_quality(file_name,file_path,destination,base_address):
    mkdir_multi(file_path,base_address,destination)

    additional_address=file_path.replace(base_address,"")
    destination_address=f'{destination}/{additional_address}/{file_name}'
    source_addr=f'{file_path}/{file_name}'
    #start loading
    src_img = Image.open(source_addr)
    width=src_img.size[0]
    if(width>width_limit):
        shrunk_img=shrink_by_width(src_img)
        shrunk_img.save(destination_address)
    else:
        src_img.save(destination_address,quality=70)


def shrink_and_copy_assets():
    for subdir, dirs, files in os.walk(asset_address):
        skip_shrinking=False
        skip_copying=False
        subdir=subdir.replace("\\","/")

        for dir_n in subdir.split("/"):

            if dir_n in folders_to_skip_shrinking:
                skip_shrinking=True
            if dir_n in folders_to_skip_copying:
                skip_copying=True

        if skip_copying:
            continue
        for file in files:
            ext=file[file.rfind(".")+1:].lower()
            # print(ext)
            if ext not in img_exts:
                copy_file(file,subdir,export_address,asset_address)
            else:
                size=os.stat(os.path.join(subdir,file)).st_size
                if(size)<size_limit and not skip_shrinking:
                    copy_file(file,subdir,export_address,asset_address)
                else:
                    shrink_image_size_quality(file,subdir,export_address,asset_address)


asset_address="../assets/local/"
export_address="../assets/web_ver/"

size_limit=1024000
width_limit=2400
folders_to_skip_shrinking=["exclude"]
folders_to_skip_copying=["exclude"]
img_exts=["jpg","png"]


shrink_and_copy_assets()

