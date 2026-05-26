from PIL import Image, ImageOps

# Open the original extracted PNG
img = Image.open("logo_light.png").convert("L")

# Invert to get alpha mask (black becomes white/opaque, white becomes black/transparent)
alpha = ImageOps.invert(img)
# Threshold the alpha to remove subtle background noise (e.g. 254 instead of 255)
alpha = alpha.point(lambda p: p if p > 50 else 0)

# Create a temporary RGBA image to find the bounding box
tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
tmp.putalpha(alpha)
bbox = tmp.getbbox()

# Crop to the bounding box
img_cropped = img.crop(bbox)
alpha_cropped = alpha.crop(bbox)

# Resize to width 400
ratio = img_cropped.width / img_cropped.height
new_width = 400
new_height = int(new_width / ratio)

# Resize both image and alpha mask using high-quality resampling
img_resized = img_cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
alpha_resized = alpha_cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Create LIGHT version: Black text, transparent background
# But wait, original img_resized has grayscale colors.
# We actually want the text to be black, but keep anti-aliasing.
# So color is black (0,0,0) and alpha is alpha_resized.
light = Image.new("RGBA", img_resized.size, (0, 0, 0, 0))
light.putalpha(alpha_resized)
light.save("logo-light.png", optimize=True)

# Create DARK version: White text, transparent background
dark = Image.new("RGBA", img_resized.size, (255, 255, 255, 0))
dark.putalpha(alpha_resized)
dark.save("logo-dark.png", optimize=True)

print(f"Logos generated! Cropped from {bbox}. Final size: {new_width}x{new_height}")
