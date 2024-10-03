import os
import time
import json
import random
import colorsys
from PIL import Image
import csv

# Directories to store color swatches and palettes
SWATCH_DIR = 'color_swatches'
PALETTE_DIR = 'color_palettes'
MEMORY_FILE = 'generated_colors.json'

# Ensure the directories exist
os.makedirs(SWATCH_DIR, exist_ok=True)
os.makedirs(PALETTE_DIR, exist_ok=True)

# Function to load or create memory of generated colors
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {'swatches': {}, 'palettes': {}}

# Function to save memory of generated colors
def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

# Load existing memory
generated_colors = load_memory()

# Base colors
base_colors = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
    "#F7DC6F", "#BB8FCE", "#82E0AA", "#F1948A", "#85C1E9",
    "#FF69B4", "#20B2AA", "#FFA500", "#9370DB", "#3CB371"
]

# Function to convert HSV to RGB
def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)

# Function to generate pastel color
def generate_pastel_color():
    h = random.random()
    s = random.uniform(0.2, 0.5)
    v = random.uniform(0.8, 1.0)
    r, g, b = hsv_to_rgb(h, s, v)
    return f"#{r:02X}{g:02X}{b:02X}"

# Function to generate neon color
def generate_neon_color():
    h = random.random()
    s = random.uniform(0.8, 1.0)
    v = random.uniform(0.8, 1.0)
    r, g, b = hsv_to_rgb(h, s, v)
    return f"#{r:02X}{g:02X}{b:02X}"

# Function to generate a new color
def generate_color():
    color_type = random.choice(['base', 'pastel', 'neon'])
    
    if color_type == 'base':
        color = random.choice(base_colors)
    elif color_type == 'pastel':
        color = generate_pastel_color()
    else:  # neon
        color = generate_neon_color()
    
    return color, color_type

# Function to generate a new palette
def generate_palette():
    palette_type = random.choice(['base', 'pastel', 'neon', 'mixed'])
    palette = []
    
    if palette_type == 'mixed':
        palette = [generate_color()[0] for _ in range(5)]
    else:
        for _ in range(5):
            color, _ = generate_color()
            while color in palette:
                color, _ = generate_color()
            palette.append(color)
    
    return palette, palette_type

# Function to save color as PNG
def save_color_as_png(color, filename):
    img_size = 100
    img = Image.new('RGB', (img_size, img_size), color)
    img.save(filename)

# Function to save palette as PNG
def save_palette_as_png(palette, filename):
    img_width = 500
    img_height = 100
    img = Image.new('RGB', (img_width, img_height))
    
    for i, color in enumerate(palette):
        for x in range(i*100, (i+1)*100):
            for y in range(img_height):
                img.putpixel((x, y), tuple(int(color[j:j+2], 16) for j in (1, 3, 5)))
    
    img.save(filename)

# Add this function to generate a JSON file with color information
def generate_color_json():
    color_data = {
        'swatches': [],
        'palettes': []
    }
    
    for color, color_type in generated_colors['swatches'].items():
        color_data['swatches'].append({
            'hex': color,
            'type': color_type,
            'filename': f"{color[1:]}_{color_type}.png"
        })
    
    for palette, palette_type in generated_colors['palettes'].items():
        colors = palette.split(',')
        color_data['palettes'].append({
            'colors': colors,
            'type': palette_type,
            'filename': f"{palette_type}_{int(time.time())}.png"
        })
    
    with open('color_data.json', 'w') as f:
        json.dump(color_data, f)

# Modify the main loop to generate the JSON file periodically
try:
    counter = 0
    while True:
        # Generate and save individual color swatch
        new_color, color_type = generate_color()
        if new_color not in generated_colors['swatches']:
            generated_colors['swatches'][new_color] = color_type
            filename = os.path.join(SWATCH_DIR, f"{new_color[1:]}_{color_type}.png")
            save_color_as_png(new_color, filename)
            print(f"Generated new {color_type} color: {new_color}")

        # Generate and save color palette
        new_palette, palette_type = generate_palette()
        palette_key = ','.join(new_palette)
        if palette_key not in generated_colors['palettes']:
            generated_colors['palettes'][palette_key] = palette_type
            filename = os.path.join(PALETTE_DIR, f"{palette_type}_{int(time.time())}.png")
            save_palette_as_png(new_palette, filename)
            print(f"Generated new {palette_type} palette: {new_palette}")

        # Save memory periodically
        save_memory(generated_colors)
        
        counter += 1
        if counter % 10 == 0:  # Generate JSON every 10 iterations
            generate_color_json()
        
        time.sleep(0.1)  # Add a small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("Script stopped by user.")
    save_memory(generated_colors)
    generate_color_json()  # Generate JSON file before exiting
    print(f"Total unique colors generated: {len(generated_colors['swatches'])}")
    print(f"Total unique palettes generated: {len(generated_colors['palettes'])}")