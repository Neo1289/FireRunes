import pygame

# Initialize Pygame
pygame.init()

# Load the image
image_path = r"C:\Users\nrade\Desktop\FireRunes\resources\wizard\0.jpg"
image = pygame.image.load(image_path)

# Get dimensions of the image
width, height = image.get_size()
print(f"Image size: {width}x{height}")

# Input pixel location
x = int(input(f"Enter X coordinate (0 to {width - 1}): "))
y = int(input(f"Enter Y coordinate (0 to {height - 1}): "))

# Get and print RGB color
if 0 <= x < width and 0 <= y < height:
    pixel_color = image.get_at((x, y))
    print(f"RGB Color at ({x}, {y}): {pixel_color[:3]}")
else:
    print("Coordinates are out of bounds.")

pygame.quit()
