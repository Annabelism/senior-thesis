import os
from PIL import Image
import matplotlib.pyplot as plt
from data100 import data

# Increase the maximum number of pixels allowed
Image.MAX_IMAGE_PIXELS = None  # This disables the limit entirely. You can also set it to a specific large number.

# Function to get the height of an image
def get_image_height(image_path):
    try:
        with Image.open(image_path) as img:
            return img.size[1]  # Height is the second element
    except FileNotFoundError:
        return None

# Function to plot the data
def plot_data(bias_ratings, height_differences, factual_ratings):
    colors = {'VERY HIGH': 'blue', 'HIGH': 'green', 'MIXED': 'yellow', 'LOW': 'orange', 'VERY LOW': 'red'}
    plt.scatter(bias_ratings, height_differences, c=[colors[rating] for rating in factual_ratings])
    plt.xlabel('Bias Rating')
    plt.ylabel('Difference in Height')
    plt.title('Bias Rating vs Difference in Screenshot Height')
    plt.show()

# Main processing loop
bias_ratings = []
height_differences = []
factual_ratings = []

for site in data:
    site_name = site['site_name'].replace(' ', '_')
    regular_screenshot = f'concatenated_shots/{site_name}.png'
    no_ad_screenshot = f'concatenated_shots/no_ad_{site_name}.png'

    regular_height = get_image_height(regular_screenshot)
    no_ad_height = get_image_height(no_ad_screenshot)

    if regular_height is None or no_ad_height is None:
        missing_files = []
        if regular_height is None:
            missing_files.append(regular_screenshot)
        if no_ad_height is None:
            missing_files.append(no_ad_screenshot)
        print(f'{site["site_name"]} - Missing file(s): {", ".join(missing_files)}')
        continue

    height_difference = regular_height - no_ad_height
    height_differences.append(height_difference)
    bias_ratings.append(int(site['bias_rating']))
    factual_ratings.append(site['factual_reporting_rating'])

# Plot the data
plot_data(bias_ratings, height_differences, factual_ratings)
