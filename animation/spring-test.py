from PIL import Image, ImageDraw, ImageSequence
import math

# Function to create a single frame
def create_frame(y1, y2, y3):
    frame = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(frame)

    # Draw a circle (red)
    draw.ellipse([125, y1, 175, y1 + 50], fill="red")

    # Draw a triangle (green)
    triangle_points = [(125, y2), (175, y2), (150, y2 + 50)]
    draw.polygon(triangle_points, fill="green")

    # Draw a hexagon (blue)
    hexagon_points = [
        (125, y3), (175, y3),
        (200, y3 + 25), (175, y3 + 50),
        (125, y3 + 50), (100, y3 + 25)
    ]
    draw.polygon(hexagon_points, fill="blue")

    # Draw the springs (lines)
    draw.line([(150, y1 + 50), (150, y2)], fill="black")
    draw.line([(150, y2 + 50), (150, y3)], fill="black")

    return frame

# Constants
fps = 30
total_duration = 10
num_frames = fps * total_duration
k = 5.0  # Spring constant
mass = 1  # Mass of objects
initial_displacement = 30

# Initialize the displacement, velocity, and acceleration
displacement = [0, initial_displacement, 0]
velocity = [0, 0, 0]
acceleration = [0, 0, 0]

# Animate the three unique shapes connected by springs
frames = []
for _ in range(num_frames):
    # Update the acceleration based on Hooke's Law: F = -k * x
    acceleration[1] = (-k * displacement[1]) / mass

    # Update the velocity and displacement for the middle object (green triangle)
    velocity[1] += acceleration[1] / fps
    displacement[1] += velocity[1] / fps

    # Update the y-coordinates of the objects based on their displacement
    y1 = int(50 + displacement[0])
    y2 = int(150 + displacement[1])
    y3 = int(250 + displacement[2])

    frame = create_frame(y1, y2, y3)
    frames.append(frame)

# Save the frames as a GIF
frames[0].save("spring_animation.gif", save_all=True, append_images=frames[1:], duration=1000 // fps, loop=0)
