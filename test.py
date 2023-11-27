import cv2
import os
import numpy as np
from PIL import Image, ImageChops
from data10 import data

# Load images
def build_alignment(site_name, base_img, extension_img):
    h_ext, w_ext = extension_img.shape
    h_base, w_base = base_img.shape

    # Initialize the result image full of white pixels
    result_img = np.full((h_ext, w_ext), 255, dtype=np.uint8)

    segment_height = 500
    segment_width = 100
    for i in range(0, h_base, segment_height):
        # Calculate the height of the segment (handle edge case for the last segment)
        current_segment_height = min(segment_height, h_base - i)

        for j in range(0, w_base, segment_width):
            # Calculate the width of the segment (handle edge case for the last segment)
            current_segment_width = min(segment_width, w_base - j)

            # Extract a segment from the base image
            segment = base_img[i:i+current_segment_height, j:j+current_segment_width]

            # Template matching to find this segment in the extension image
            result = cv2.matchTemplate(extension_img, segment, cv2.TM_CCOEFF_NORMED)

            # Find all locations where matches exceed the threshold
            loc = np.where(result >= 0.8)
            for pt in zip(*loc[::-1]):  # Switch x and y coordinates
                x, y = pt

                # Ensure we don't go beyond the extension image's boundaries
                if y + current_segment_height > h_ext or x + current_segment_width > w_ext:
                    continue

                # Paste the segment into the result image
                result_img[y:y+current_segment_height, x:x+current_segment_width] = segment

    # Save or show the result
    cv2.imwrite(f'aligned/aligned_{site_name}.png', result_img)


def create_diff(site_name):
    image1 = Image.open(f'aligned/aligned_{site_name}.png')
    image2 = Image.open(f'concatenated_shots/no_ad_{site_name}.png')
    image1 = image1.convert('RGB')
    image2 = image2.convert('RGB')
    diff = ImageChops.difference(image1, image2)

    # Convert the PIL Image to a NumPy array
    diff_np = np.array(diff)
    # OpenCV expects the image in BGR format, convert if necessary
    if diff_np.shape[2] == 3:  # If it's a 3-channel image
        diff_np = cv2.cvtColor(diff_np, cv2.COLOR_RGB2BGR)

    cv2.imwrite(f'difference/diff_{site_name}.png', diff_np)

for x in data:
    site = x["site_name"].replace(" ", "_")
    image_path = f'concatenated_shots/{site}.png'
    if os.path.exists(image_path):
        base = cv2.imread(f'concatenated_shots/{site}.png', 0)
        extension = cv2.imread(f'concatenated_shots/no_ad_{site}.png', 0)
        build_alignment(site, base, extension)
        create_diff(site)