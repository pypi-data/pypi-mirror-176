# Split an image into equal parts

<img src="https://github.com/hansalemaos/screenshots/raw/main/splitted1.jpeg"/>
<img src="https://github.com/hansalemaos/screenshots/raw/main/splitted1.png"/>
<img src="https://github.com/hansalemaos/screenshots/raw/main/splitted0.png"/>


```python

import cv2
from a_cv2_split_images_into_equal_parts import add_split_images_to_cv2
add_split_images_to_cv2()
list_pics,list_files=cv2.split_image_into_equal_parts(
    img=r"https://github.com/hansalemaos/screenshots/raw/main/splitted1.jpeg",
    outputfolder="f:\\picsplittedxxx",
    pixel_width=100,
    pixel_height=200,
    colorborder=(255, 0, 0),
    text_color_border1=(0, 150, 0),
    text_color_border2=(200, 0, 0),
    text_height_1=0.4,
    text_height_2=0.4, )

In[3]: list_pics
Out[3]: 
[array([[[145, 170, 144],
         [145, 170, 144],
         [145, 170, 144],
         ...,
         [113, 149, 119],
         [112, 148, 118],
         [114, 150, 120]],
 
        [[145, 170, 144],
         [145, 170, 144],
         [145, 170, 144],
         ...,
         [112, 148, 118],
         [112, 148, 118],
         [113, 149, 119]],
		 ....
list_files
Out[4]: 
['f:\\picsplittedxxx\\splitted\\0x0-100x200.png',
 'f:\\picsplittedxxx\\splitted\\0x200-100x400.png',
 'f:\\picsplittedxxx\\splitted\\0x400-100x750.png',
 'f:\\picsplittedxxx\\splitted\\100x0-200x200.png',
 'f:\\picsplittedxxx\\splitted\\100x200-200x400.png',
 'f:\\picsplittedxxx\\splitted\\100x400-200x750.png',
 'f:\\picsplittedxxx\\splitted\\200x0-300x200.png',
 'f:\\picsplittedxxx\\splitted\\200x200-300x400.png',
 'f:\\picsplittedxxx\\splitted\\200x400-300x750.png',
 ....


import cv2
from a_cv2_split_images_into_equal_parts import add_split_images_to_cv2
add_split_images_to_cv2()
list_pics,list_files=cv2.split_image_into_equal_parts(
    img=r"https://github.com/hansalemaos/screenshots/raw/main/splitted1.jpeg",
    outputfolder=None,
    pixel_width=100,
    pixel_height=200,
    colorborder=(255, 0, 0),
    text_color_border1=(0, 150, 0),
    text_color_border2=(200, 0, 0),
    text_height_1=0.4,
    text_height_2=0.4, )
In[3]: list_pics
Out[3]: 
[array([[[145, 170, 144],
         [145, 170, 144],
         [145, 170, 144],
         ...,
         [113, 149, 119],
         [112, 148, 118],
         [114, 150, 120]],
 
        [[145, 170, 144],
         [145, 170, 144],
         [145, 170, 144],
         ...,
         [112, 148, 118],
         [112, 148, 118],
         [113, 149, 119]],
		 ....
```