import random
from PIL import Image, ImageDraw
import argparse
from bokeh.palettes import inferno
from tqdm import tqdm
import math
import zipfile
import io


class ShapeInfo:
    """ A class to store information about a shape. """
    def __init__(self, shape, x, y, color, angle=None):
        self.shape = shape
        self.x = x
        self.y = y
        self.color = color
        self.angle = angle


def random_color(palette=inferno(256)):
    """ Return a random color from a palette."""
    return random.choice(palette)


def is_shape_overlapping(existing_shapes, new_shape, min_distance):
    """ Check if a new shape is overlapping with existing shapes. """
    for shape in existing_shapes:
        x1, y1, x2, y2 = shape
        distance = math.sqrt((x1 - new_shape[0]) ** 2 + (y1 - new_shape[1]) ** 2)
        if distance < min_distance:
            return True
    return False


def direction_angle(x1, y1, x2, y2):
    """ Return the angle between two points. """
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 360
    return angle


def direction_name(angle):
    """ Return the name of the direction given an angle. """
    directions = ["right", "bottom-right", "bottom", "bottom-left", "left", "top-left", "top", "top-right"]
    index = round(angle / 45) % 8
    return directions[index]


def generate_knowledge_graph(shapes_info: list) -> str:
    """ Generate a knowledge graph in the form of a string. """

    graph = []
    for i, shape_info in enumerate(shapes_info):
        graph.append(f"Element_{i + 1} has_shape {shape_info.shape}.")
        graph.append(f"Element_{i + 1} has_colour {shape_info.color}.")
        graph.append(f"Element_{i + 1} has_position ({shape_info.x}, {shape_info.y}).")

        for j, other_shape_info in enumerate(shapes_info):
            if i != j:
                angle = direction_angle(shape_info.x, shape_info.y, other_shape_info.x, other_shape_info.y)
                direction = direction_name(angle)
                graph.append(f"Element_{i + 1} is_positioned_{direction}_of Element_{j + 1}.")

    return "\n".join(graph)


def is_shape_overlapping(existing_shapes, new_shape, min_distance):
    for shape in existing_shapes:
        x1, y1, x2, y2 = shape
        distance = math.sqrt((x1 - new_shape[0]) ** 2 + (y1 - new_shape[1]) ** 2)
        if distance < min_distance:
            return True
    return False


def regular_polygon_vertices(sides, x, y, size):
    angle = 2 * 3.14159 / sides
    return [(x + size * 0.5 * math.cos(i * angle), y + size * 0.5 * math.sin(i * angle)) for i in range(sides)]


def generate_shapes_image(num_elements: int, width: int, height: int) -> (Image.Image, list):
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    shape_size = 50
    min_distance = 20
    existing_shapes = []

    shapes_info = []

    for _ in range(num_elements):
        shape = random.choice(["rectangle", "circle", "triangle", "pentagon", "hexagon",
                               "heptagon", "octagon", "nonagon", "decagon", "rhombus"])
        color = random_color()

        while True:
            x, y = random.randint(0, width - shape_size), random.randint(0, height - shape_size)
            if not is_shape_overlapping(existing_shapes, (x, y, x + shape_size, y + shape_size), min_distance + shape_size):
                break

        existing_shapes.append((x, y, x + shape_size, y + shape_size))
        shape_info = ShapeInfo(shape, x, y, color)

        if shape == "rectangle":
            draw.rectangle([x, y, x + shape_size, y + shape_size], fill=color)
        elif shape == "circle":
            draw.ellipse([x, y, x + shape_size, y + shape_size], fill=color)
        elif shape == "triangle":
            draw.polygon([(x, y), (x + shape_size, y), (x + shape_size // 2, y + shape_size)], fill=color)
        elif shape == "rhombus":
            draw.polygon([(x + shape_size // 2, y), (x + shape_size, y + shape_size // 2),
                          (x + shape_size // 2, y + shape_size), (x, y + shape_size // 2)], fill=color)
        else:
            sides = {"pentagon": 5, "hexagon": 6, "heptagon": 7, "octagon": 8, "nonagon": 9, "decagon": 10}
            vertices = regular_polygon_vertices(sides[shape], x + shape_size // 2, y + shape_size // 2, shape_size)
            draw.polygon(vertices, fill=color)

        shapes_info.append(shape_info)

    return img, shapes_info


def save_images(total_images: int, num_elements: int, width: int, height: int, seed: int, split_ratios: tuple):
    """ Save images and knowledge graphs in a zip file."""
    random.seed(seed)
    zip_filename = f"SSGG{num_elements}_{total_images}_({width}x{height})_seed{seed}.zip"

    with zipfile.ZipFile(zip_filename, "w") as zipped_shapes:
        train_size, valid_size, _ = [int(ratio * total_images) for ratio in split_ratios]

        for split, size in zip(["train", "valid", "test"],
                               [train_size, valid_size, total_images - train_size - valid_size]):
            for i in tqdm(range(size), desc="Generating images"):
                img, shapes_info = generate_shapes_image(num_elements, width, height)
                image_filename = f"{split}/image_{i}.jpg"
                knowledge_graph_filename = f"{split}/knowledge_graph_{i}.txt"

                with zipped_shapes.open(image_filename, "w") as image_file:
                    img.save(image_file, "JPEG")
                with zipped_shapes.open(knowledge_graph_filename, "w") as kg_file:
                    kg = generate_knowledge_graph(shapes_info)
                    kg_file.write(kg.encode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images with simple shapes and unique colors.")
    parser.add_argument("--num_images", type=int, default=1, help="Number of images to generate (default: 1).")
    parser.add_argument("--num_elements", type=int, default=5,
                        help="Number of unique elements (shapes) in each image (default: 5).")
    parser.add_argument("--width", type=int, default=500, help="Width of the generated images (default: 500).")
    parser.add_argument("--height", type=int, default=500, help="Height of the generated images (default: 500).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42).")
    parser.add_argument("--split_ratios", type=float, nargs=3, default=(0.7, 0.2, 0.1), help="Split ratios for train, valid, and test sets, respectively (default: 0.7,0.2,0.1).")
    args = parser.parse_args()
    save_images(args.num_images, args.num_elements, args.width, args.height, args.seed, args.split_ratios)
