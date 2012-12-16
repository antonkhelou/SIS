from django.conf import settings
from django.shortcuts import render
from PIL import Image

from utils import *
import os


def home(request):
    pixel_block_size = 16 # for pixelation process
    segment_width = 8 
    num_segmented_images = 8
    image_path = os.path.join(settings.MEDIA_ROOT, "fantasy1920x1200.jpg")
    pixelated_img_name = "fantasy1920x1200pix%dby%d.jpg" % (pixel_block_size, pixel_block_size)


    print image_path
    # make the image segments from the source image
    segmented_images = segment_image(image_path, segment_width, num_segmented_images)

    # the following create a pixelated version of the image
    pixelated_image = nn_resample_image(image_path, pixel_block_size, pixel_block_size)

    width, height = pixelated_image.size

    pixelated_image.save(os.path.join(settings.MEDIA_ROOT, pixelated_img_name), format="JPEG")

    segmented_images_paths = []
    for index, seg_img in enumerate(segmented_images):
        seg_img_file_name = "fantasy1920x1200seg%s.jpg" % index
        seg_img.save(os.path.join(settings.MEDIA_ROOT, seg_img_file_name), format="JPEG")
        segmented_images_paths.append(os.path.join(settings.MEDIA_URL, seg_img_file_name))

    data = {
        "width": width,
        "height": height,
        "segment_width": segment_width,
        "num_segmented_images": num_segmented_images,
        "segmented_images_paths": segmented_images_paths,
        "pixelated_img_path": os.path.join(settings.MEDIA_URL, pixelated_img_name),
    }

    return render(request, 'main/home.html', data)