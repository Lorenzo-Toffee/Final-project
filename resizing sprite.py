import os
from PIL import Image

folder = "Enemies"
output_folder = "Enemies_resized"
target_size = (500, 500)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(folder):
    if filename.endswith(".png"):
        img = Image.open(os.path.join(folder, filename))
        img_copy = img.copy()
        # Use Image.Resampling.LANCZOS for high quality or NEAREST for pixel art
        img_resized = img_copy.resize(target_size, Image.Resampling.NEAREST)
        img_resized.save(os.path.join(output_folder, filename))