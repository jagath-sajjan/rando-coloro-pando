# Color Palette Generator and Gallery

This project generates a variety of color swatches and palettes, and displays them in an interactive web gallery. It's perfect for designers, artists, or anyone looking for color inspiration.

## Features

- Generates individual color swatches and color palettes
- Includes base colors, pastel colors, and neon colors
- Displays colors in a responsive, Pinterest-like gallery
- Infinite scrolling for seamless browsing
- Download functionality for each swatch and palette
- Dark mode interface for comfortable viewing

## How to Use

1. Clone this repository:
   ```bash
   git clone https://github.com/jagath-sajjan/rando-coloro-pando.git
   ```

2. Run the color generation script:
   ```bash
   python main.py
   ```
   This will generate color swatches and palettes in the `color_swatches` and `color_palettes` directories.

3. Generate the image list:
   ```bash
   python generate_image_list.py
   ```
   This creates a JSON file with the list of all generated images.

4. Open `index.html` in a web browser to view the gallery.

## Project Structure

- `main.py`: Generates color swatches and palettes
- `generate_image_list.py`: Creates a JSON file of all generated images
- `index.html`: The main webpage
- `styles.css`: Styling for the webpage
- `script.js`: JavaScript for gallery functionality
- `color_srgb.csv`: Base colors data

## Technologies Used

- Python (for color generation)
- HTML/CSS/JavaScript (for the web gallery)
- Masonry.js (for the Pinterest-like layout)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
