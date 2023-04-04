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


def generate_knowledge_graph(shapes_info: list) -> str:
    """ Generate a knowledge graph in the form of a string. """
    def direction_angle(x1, y1, x2, y2):
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 360
        return angle

    def direction_name(angle):
        directions = ["right", "bottom-right", "bottom", "bottom-left", "left", "top-left", "top", "top-right"]
        index = round(angle / 45) % 8
        return directions[index]

    graph = []
    for i, shape_info in enumerate(shapes_info):
        graph.append(f"Element_{i + 1} has_shape {shape_info.shape}.")
        graph.append(f"Element_{i + 1} has_colour {shape_info.color}.")
        graph.append(f"Element_{i + 1} has_position ({shape_info.x}, {shape_info.y}).")
        if shape_info.angle is not None:
            graph.append(f"Element_{i + 1} has_rotation {shape_info.angle} degrees.")

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


def save_images(num_images: int, num_elements: int, width: int, height: int, seed: int):
    """ Save images and knowledge graphs in a zip file."""
    random.seed(seed)

    zip_file_name = f"SSGG_{num_elements}_{num_images}_({width}x{height})_seed{seed}.zip"

    with zipfile.ZipFile(zip_file_name, "w") as zf:
        for i in tqdm(range(num_images), desc="Generating images"):
            img, shapes_info = generate_shapes_image(num_elements, width, height)
            img_name = f"image_{i + 1}.jpg"

            with io.BytesIO() as img_buffer:
                img.save(img_buffer, "JPEG")
                img_buffer.seek(0)
                zf.writestr(img_name, img_buffer.read())

            kg_name = f"knowledge_graph_{i + 1}.txt"
            kg_content = generate_knowledge_graph(shapes_info)

            with io.BytesIO(kg_content.encode()) as kg_buffer:
                zf.writestr(kg_name, kg_buffer.read())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images with simple shapes and unique colors.")
    parser.add_argument("--num_images", type=int, default=1, help="Number of images to generate (default: 1).")
    parser.add_argument("--num_elements", type=int, default=5,
                        help="Number of unique elements (shapes) in each image (default: 5).")
    parser.add_argument("--width", type=int, default=500, help="Width of the generated images (default: 500).")
    parser.add_argument("--height", type=int, default=500, help="Height of the generated images (default: 500).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42).")
    args = parser.parse_args()
    save_images(args.num_images, args.num_elements, args.width, args.height, args.seed)
