import os
from typing import Union, Any

import cv2
from a_cv_imwrite_imread_plus import open_image_in_cv, save_cv_image


def reverse_color(color):
    if len(color) == 3:
        return list(reversed(color))
    elif len(color) == 4:
        return list(reversed(color[:3])) + [color[-1]]
    return color


def divide_number_to_generator_with_rest(number, divider):
    splittedx = divmod(number, divider)
    rangex = (
        divider if ini != splittedx[0] - 1 else divider + splittedx[-1]
        for ini, _ in enumerate(range(splittedx[0]))
    )
    return rangex


def cropimage(img, coords):
    return img[coords[1] : coords[3], coords[0] : coords[2]].copy()


def split_image_into_equal_parts(
    img: Any,
    outputfolder: Union[str,None],
    pixel_width: int = 50,
    pixel_height: int = 80,
    colorborder: tuple = (255, 0, 0),
    text_color_border1: tuple = (0, 0, 255),
    text_color_border2: tuple = (0, 255, 0),
    text_height_1: Union[float, int] = 0.4,
    text_height_2: Union[float, int] = 0.4,
) -> list:
    im = open_image_in_cv(img, channels_in_output=3).copy()
    im2 = im.copy()
    imgheight = im.shape[0]
    imgwidth = im.shape[1]
    listx = list(divide_number_to_generator_with_rest(imgwidth, pixel_width))
    listy = list(divide_number_to_generator_with_rest(imgheight, pixel_height))
    listx.insert(0, 0)
    listy.insert(0, 0)
    width = 0
    text_color_border1 = reverse_color(text_color_border1)
    text_color_border2 = reverse_color(text_color_border2)
    splitfiles = []
    splitimages = []
    for x, addx in zip(listx, listx[1:]):
        width = width + x
        height = 0
        for y, addy in zip(listy, listy[1:]):
            height = height + y
            picparts = cropimage(
                im2, coords=(width, height, width + addx, height + addy)
            ).copy()
            splitimages.append(picparts.copy())
            if outputfolder is not None:
                splitfile = os.path.join(
                    outputfolder,
                    f"splitted",
                    f"{width}x{height}-{width + addx}x{height + addy}.png",
                )
                print(splitfile, end="\r")
                splitfiles.append(splitfile)

                save_cv_image(splitfile, picparts)
                cv2.rectangle(
                    im, (width, height), (width + addx, height + addy), colorborder
                )
                cv2.putText(
                    im,
                    f"{width}x{height}",
                    (width, height + pixel_height // 8),
                    0,
                    text_height_1,
                    text_color_border1,
                    thickness=1,
                    lineType=cv2.LINE_AA,
                )
                cv2.putText(
                    im,
                    f"{width + addx}x{height + addy}",
                    (width, height + int(addy / 10 * 9)),
                    0,
                    text_height_2,
                    text_color_border2,
                    thickness=1,
                    lineType=cv2.LINE_AA,
                )
    if outputfolder is not None:
        splitfile = os.path.join(outputfolder, "whole.png")
        save_cv_image(splitfile, im)
        splitfiles.append(splitfile)
    return splitimages,splitfiles


def add_split_images_to_cv2():
    cv2.split_image_into_equal_parts = split_image_into_equal_parts


# split_image_into_equal_parts(
#     img=r"https://images.pexels.com/photos/1661179/pexels-photo-1661179.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
#     pixel_width=100,
#     pixel_height=200,
#     colorborder=(255, 0, 0),
#     text_color_border1=(0, 150, 0),
#     text_color_border2=(200, 0, 0),
#     text_height_1=0.4,
#     text_height_2=0.4,
#     outputfolder="f:\\picsplitted",
# )
