from PIL import Image

import sys


def nn_resample_image(image_path, pxl_box_width, pxl_box_height):
    """
    Function which pixelates an image by averaging out pixel values in blobs of
    pxl_box_width * pxl_box_height in dimensions.
    Returns a PIL Image object.
    """
    image = Image.open(image_path)
    if image.format == "JPEG" or image.format == "PNG":
        __nn_resample_png_jpeg_image(image, pxl_box_width, pxl_box_height)
    elif image.format == "GIF":
        __nn_resample_gif_image(image, pxl_box_width, pxl_box_height)

    return image


def __nn_resample_png_jpeg_image(image, pxl_box_width, pxl_box_height):
    '''
    Pixelation private function for PNG and JPEG images. These contain 3 values for each
    pixel (RBG).
    '''
    width, height = image.size
    img_data = image.load()

    for col_index in range(0, width, pxl_box_width):
        width_pxl_box_range = min((col_index + pxl_box_width), width)
        for row_index in range(0, height, pxl_box_height):
            average_value = [0,0,0]
            # to ensure we don't go out of bounds
            height_pxl_box_range = min((row_index + pxl_box_height), height)
            for pxl_box_col_index in range(col_index, width_pxl_box_range):
                for pxl_box_row_index in range(row_index, height_pxl_box_range):
                    pxl_rgb_tuple = img_data[pxl_box_col_index,pxl_box_row_index]
                    average_value[0] += pxl_rgb_tuple[0]
                    average_value[1] += pxl_rgb_tuple[1]
                    average_value[2] += pxl_rgb_tuple[2]

            num_pixel_values = ((width_pxl_box_range - col_index) * (height_pxl_box_range - row_index))
            average_value[0] = average_value[0] / num_pixel_values
            average_value[1] = average_value[1] / num_pixel_values
            average_value[2] = average_value[2] / num_pixel_values

            for pxl_box_col_index in range(col_index, width_pxl_box_range):
                for pxl_box_row_index in range(row_index, height_pxl_box_range):
                    img_data[pxl_box_col_index, pxl_box_row_index] = (average_value[0], average_value[1], average_value[2])


def __nn_resample_gif_image(image, pxl_box_width, pxl_box_height):
    '''
    Pixelation private function for GIF images. These contain 1 value for each pixel.
    '''
    width, height = image.size
    img_data = image.load()

    for col_index in range(0, width, pxl_box_width):
        width_pxl_box_range = min((col_index + pxl_box_width), width)
        for row_index in range(0, height, pxl_box_height):
            average_value = 0
            # to ensure we don't go out of bounds
            height_pxl_box_range = min((row_index + pxl_box_height), height)
            for pxl_box_col_index in range(col_index, width_pxl_box_range):
                for pxl_box_row_index in range(row_index, height_pxl_box_range):
                    pxl_rgb_val = img_data[pxl_box_col_index, pxl_box_row_index]
                    average_value += pxl_rgb_val

            num_pixel_values = ((width_pxl_box_range - col_index) * (height_pxl_box_range - row_index))
            average_value = average_value / num_pixel_values

            for pxl_box_col_index in range(col_index, width_pxl_box_range):
                for pxl_box_row_index in range(row_index, height_pxl_box_range):
                    img_data[pxl_box_col_index, pxl_box_row_index] = average_value


def segment_image(image_path, segment_width, num_segmented_images):
    '''
    Function which chops up an image into segments. The number of segments is determined by
    the segment_width parameter and num_segmented_images. The segmented images are created by
    chopping the original image segment by segment and storing them into different segmented
    images(determined by num_segmented_images parameter) in a round robin fashion. The images
    which are returned are PIL Image objects.
    '''
    original_image = Image.open(image_path)
    width, height = original_image.size
    original_img_data = original_image.load()

    segmented_images = \
        [Image.new(original_image.mode, (width/num_segmented_images, height)) for i in range(num_segmented_images)]

    width_increment = (segment_width * num_segmented_images) # used for the nested for

    for row_index in range(0, height):
        current_seg_col_index = 0
        for col_index in range(0, width, width_increment):
            # to ensure we don't go out of bounds
            width_pxl_box_range = min((col_index + width_increment), width)

            for i in range(num_segmented_images):
                seg_img_data = segmented_images[i].load()
                col_count = 0
                for orig_col_index in range(col_index + (i*segment_width), col_index + ((i+1)*segment_width)):
                    seg_img_data[current_seg_col_index + col_count, row_index] = \
                        original_img_data[orig_col_index, row_index]
                    col_count = col_count + 1

            current_seg_col_index = current_seg_col_index + segment_width

    return segmented_images


def pixelate_datasets():
    '''
    This function will pixelate all images located under the sis/datasets directory.
    Upon completion, it will return a string where each line represents results for one file of the format:
                    filename    original_size_in_mb     pixelated_size_in_mb
    '''
    import os
    from django.conf import settings

    output_string = ""

    walk = os.walk(os.path.join(settings.PROJECT_DIR, "datasets/"))

    for root, dirs, files in walk:

        # ignore the pixalted folders where the results are stored
        if 'pixelated8x8' in dirs:
            dirs.remove('pixelated8x8')

        if 'pixelated16x16' in dirs:
            dirs.remove('pixelated16x16')

        for f in files:
            if not os.path.exists(os.path.join(root, "pixelated8x8")):
                os.makedirs(os.path.join(root, "pixelated8x8"))

            if not os.path.exists(os.path.join(root, "pixelated16x16")):
                os.makedirs(os.path.join(root, "pixelated16x16"))

            fullpath = os.path.join(root, f)

            output_string = output_string + f + "\t" + str((os.path.getsize(os.path.join(root, f)) / (1024 * 1024.0)))
            
            print fullpath

            # perform 8x8 pixelation
            img = Image.open(fullpath)
            nn_resample_image(img, 8, 8)
            img.save(os.path.join(os.path.join(root, "pixelated8x8"), f))

            output_string = output_string + "\t" + str((os.path.getsize(os.path.join(os.path.join(root, "pixelated8x8"), f)) / (1024 * 1024.0)))

            # perform 16x16 pixelation
            img = Image.open(fullpath)
            nn_resample_image(img, 16, 16)
            img.save(os.path.join(os.path.join(root, "pixelated16x16"), f))

            output_string = output_string + "\t" + str((os.path.getsize(os.path.join(os.path.join(root, "pixelated16x16"), f)) / (1024 * 1024.0))) + "\n"

    return output_string