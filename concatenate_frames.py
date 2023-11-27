from PIL import Image
import numpy as np
import os
from data100  import data


def load_images(filename):
    images = []
    i = 1
    while True:
        image_path = f"screenshots/{filename}_{i}.png"
        if os.path.exists(image_path):
            images.append(Image.open(image_path))
            i += 1
        else:
            # Stop if no more images are found
            break
    return images

def find_overlap(img1, img2):
    img1_np = np.array(img1)
    img2_np = np.array(img2)
    overlap = 0
    
    # Only check the overlap if images are of the same width
    if img1_np.shape[1] == img2_np.shape[1]:        
        # Scan for overlap from the bottom of img1 and the top of img2
        # to find the maximal vertical overlap.
        for y in range(1, min(img1_np.shape[0], img2_np.shape[0])):
            if np.array_equal(img1_np[-y:], img2_np[:y]):
                overlap = y
                
    return overlap

def concatenate_images(images):
    total_width = max(img.width for img in images)
    total_height = sum(img.height for img in images) - sum(find_overlap(images[i], images[i+1]) for i in range(len(images)-1))
    
    new_image = Image.new('RGB', (total_width, total_height))
    y_offset = 0
    
    for i in range(len(images)-1):
        img1 = images[i]
        img2 = images[i+1]
        
        overlap = find_overlap(img1, img2)
        
        new_image.paste(img1, (0, y_offset))
        y_offset += img1.height - overlap
    
    # Paste the last image
    new_image.paste(images[-1], (0, y_offset))
    
    return new_image

def main():
    for site_dict in data:
        site_name = site_dict['site_name'].replace(" ", "_")
        images = load_images(site_name)
        if images:
            concatenated_image = concatenate_images(images)
            concatenated_image_path = f'concatenated_shots/{site_name}.png'
            concatenated_image.save(concatenated_image_path, 'PNG')
            print(f"Image concatenation for {site_name} complete!")
        else:
            print(f"No images loaded for {site_name}")

        images = load_images("no_ad_"+site_name)
        if images:
            concatenated_image = concatenate_images(images)
            concatenated_image_path = f'concatenated_shots/no_ad_{site_name}.png'
            concatenated_image.save(concatenated_image_path, 'PNG')
            print(f"Image concatenation for no-ad {site_name} complete!")
        else:
            print(f"No images loaded for {site_name}")

if __name__ == "__main__":
    main()