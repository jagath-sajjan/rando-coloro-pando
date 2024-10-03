import os
import json

def list_images(directory):
    return [f for f in os.listdir(directory) if f.endswith('.png')]

swatch_images = list_images('color_swatches')
palette_images = list_images('color_palettes')

image_data = {
    'swatches': swatch_images,
    'palettes': palette_images
}

with open('image_list.json', 'w') as f:
    json.dump(image_data, f)

print("image_list.json has been generated.")