import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import datetime

# Load Patreon data saved by fetch_patrons.py
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
filename = f'active_patrons_10_above_{current_date}.csv'
active_10_above_df = pd.read_csv(filename)

# Generate an image
image_width = 1920
text_y_position = 800  # Starting Y position for the first text
text_padding = 120  # Padding between text lines
font_size = 100
image_height = (len(active_10_above_df) * text_padding) + (text_y_position * 2)
img = Image.new('RGB', (image_width, image_height), color=(58, 63, 68))
draw = ImageDraw.Draw(img)

# Set up font and size
font_path = "C:\\Windows\\Fonts\\arial.ttf"  # Adjust with the actual path to your font
fnt = ImageFont.truetype(font_path, font_size)

# Manually estimate the width of each character. This is a rough approximation.
approx_char_width = font_size * 0.6

# Draw text from DataFrame
for index, name in enumerate(active_10_above_df['Full Name']):
    # Calculate approximate text width
    text_width = len(name) * approx_char_width
    text_x_position = (image_width - text_width) // 2  # Center horizontally
    
    # Draw text onto the image
    draw.text((text_x_position, text_y_position), name, font=fnt, fill=(255, 255, 255))
    
    # Increment the Y position for the next name
    text_y_position += text_padding

# Save the image with dynamic filename
image_path = f"patrons_credits_{current_date}.png"
img.save(image_path)

print(f"Image saved as {image_path}")
