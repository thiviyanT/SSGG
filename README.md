<p  align="center">
    <img src="images/ssgg-logo.png" alt="Alt text describing the logo" width="150px;" style="max-width: 100%;  margin-right:10px;">
<p>
<h1 align="center" dir="auto" style="font-size:60px;">
    Simple Scene Graph Generator (SSGG)
</h1>

This Python script generates images containing simple shapes with unique colors. The script allows you to specify the number of images and the number of elements (shapes) in each image.

## TODO

- [ ] Modify script so that each shape only apears once in each image.
- [ ] Gurantee that the splits are not overlapping.
- [ ] Variable number of elements per image.
- [ ] Create different variations of this dataset.

## Task

The SSGG dataset generated by this script can be used to investigate the spatial reasoning capabilities of generative models. The images contain simple shapes with varying positions and colors, and the knowledge graphs describe the spatial relationships between these shapes. By training a generative model on this dataset, researchers can evaluate the model's ability to understand, learn, and predict spatial relationships between objects, which is a crucial aspect of many real-world applications, such as robotics, autonomous vehicles, and scene understanding.


## Installation

To install the required packages, run the following command:

```bash
pip install pillow bokeh tqdm
```

## Usage

To run the script, use the following command:

```bash
python generate_shapes.py --num_images=10 --num_elements=5
```
This command will generate 10 images, each containing 5 shapes with random rotations.

Arguments
* `--num_images`: The number of images to generate (default: 1).
* `--num_elements`: The number of unique elements (shapes) to include in each image (default: 5).
* `--width`: The width of the generated images (default: 500).
* `--height`: The height of the generated images (default: 500).
* `--seed`: The random seed to use (default: 42).

## Knowledge Graph

The knowledge graph is a textual representation of the spatial relationships between elements (shapes) in an image. It consists of statements describing attributes and relative positions of elements:

1. **Unique Identifier**: `element_{i}`, where `{i}` is the index of the element.
2. **Attributes**:
    - `element_{i} has_shape {shape}`: Shape of the element (e.g., circle, square, triangle).
    - `element_{i} has_position {position}`: Position (x, y) of the element.
    - `element_{i} has_colour {color}`: Color of the element (from Bokeh Inferno palette).
3. **Relative Positions**:
    - `element_{i} is_positioned_{direction}_of element_{j}`: Relative position of `{i}` with respect to `{j}`. `{direction}` can be: left, right, above, below, top_left, top_right, bottom_left, or bottom_right.

Each statement is on a separate line. The knowledge graph provides a structured, human-readable description of the spatial relationships between elements, useful for training and evaluating generative models on spatial reasoning tasks.

## Checking Semantics
To check the semantics of the knowledge graphs generated by the generate_shapes.py script, you can run the check_semantics.py script. This script takes a knowledge graph file as input and checks that the relations and entities in the graph are valid.

To run the script, you can use the following command:

```
python check_semantics.py <knowledge_graph_file>
```

Replace <knowledge_graph_file> with the path to a knowledge graph file. The script will print out any errors it finds in the knowledge graph.

## Output

The output of the `generate_shapes.py` script is a zipped folder containing the generated images and corresponding knowledge graphs. Each image contains the specified number of unique colored shapes, and the knowledge graph describes the shapes, their positions, and colors.

The zip file is named concisely to include the random seed, number of elements, and the height and width of the images, e.g., `SSGG5_10000_(500x500)_seed42.zip`.

### Data Split
The generate_shapes.py script generates three splits of the dataset: train, validation, and test. By default, the script generates 70% of the images for the train split, 20% for the validation split, and 10% for the test split.

## Examples

<table>
  <tr>
    <th>Image</th>
    <th>Knowledge Graph</th>
  </tr>
  <tr>
    <td><img src="examples/image_1.jpg" alt="Example Image 1"></td>
    <td><pre>
Element_1 has_shape octagon.
Element_1 has_colour #C93F4A.
Element_1 has_position (303, 107).
Element_1 is_positioned_top-left_of Element_2.
Element_1 is_positioned_bottom-left_of Element_3.
Element_1 is_positioned_left_of Element_4.
Element_1 is_positioned_bottom_of Element_5.
Element_2 has_shape octagon.
Element_2 has_colour #BF3951.
Element_2 has_position (181, 10).
Element_2 is_positioned_bottom-right_of Element_1.
Element_2 is_positioned_bottom-left_of Element_3.
Element_2 is_positioned_bottom-left_of Element_4.
Element_2 is_positioned_bottom-right_of Element_5.
Element_3 has_shape pentagon.
Element_3 has_colour #62146E.
Element_3 has_position (29, 279).
Element_3 is_positioned_top-right_of Element_1.
Element_3 is_positioned_top-right_of Element_2.
Element_3 is_positioned_top-right_of Element_4.
Element_3 is_positioned_right_of Element_5.
Element_4 has_shape decagon.
Element_4 has_colour #8E2468.
Element_4 has_position (109, 137).
Element_4 is_positioned_right_of Element_1.
Element_4 is_positioned_top-right_of Element_2.
Element_4 is_positioned_bottom-left_of Element_3.
Element_4 is_positioned_right_of Element_5.
Element_5 has_shape decagon.
Element_5 has_colour #F57E14.
Element_5 has_position (325, 180).
Element_5 is_positioned_top_of Element_1.
Element_5 is_positioned_top-left_of Element_2.
Element_5 is_positioned_left_of Element_3.
Element_5 is_positioned_left_of Element_4.
    </pre></td>
  </tr>
  <tr>
    <td><img src="examples/image_2.jpg" alt="Example Image 2"></td>
    <td><pre>
Element_1 has_shape octagon.
Element_1 has_colour #FABD23.
Element_1 has_position (90, 202).
Element_1 is_positioned_right_of Element_2.
Element_1 is_positioned_top_of Element_3.
Element_1 is_positioned_right_of Element_4.
Element_1 is_positioned_top_of Element_5.
Element_2 has_shape circle.
Element_2 has_colour #F7FB99.
Element_2 has_position (241, 219).
Element_2 is_positioned_left_of Element_1.
Element_2 is_positioned_top-left_of Element_3.
Element_2 is_positioned_top_of Element_4.
Element_2 is_positioned_top-left_of Element_5.
Element_3 has_shape circle.
Element_3 has_colour #801F6B.
Element_3 has_position (31, 53).
Element_3 is_positioned_bottom_of Element_1.
Element_3 is_positioned_bottom-right_of Element_2.
Element_3 is_positioned_right_of Element_4.
Element_3 is_positioned_right_of Element_5.
Element_4 has_shape pentagon.
Element_4 has_colour #C13A50.
Element_4 has_position (273, 133).
Element_4 is_positioned_left_of Element_1.
Element_4 is_positioned_bottom_of Element_2.
Element_4 is_positioned_left_of Element_3.
Element_4 is_positioned_top-left_of Element_5.
Element_5 has_shape decagon.
Element_5 has_colour #FABB21.
Element_5 has_position (104, 31).
Element_5 is_positioned_bottom_of Element_1.
Element_5 is_positioned_bottom-right_of Element_2.
Element_5 is_positioned_left_of Element_3.
Element_5 is_positioned_bottom-right_of Element_4.
    </pre></td>
  </tr>
  <tr>
    <td><img src="examples/image_3.jpg" alt="Example Image 3"></td>
    <td><pre>
Element_1 has_shape hexagon.
Element_1 has_colour #0F092D.
Element_1 has_position (131, 238).
Element_1 is_positioned_bottom-right_of Element_2.
Element_1 is_positioned_top-left_of Element_3.
Element_1 is_positioned_right_of Element_4.
Element_1 is_positioned_top-right_of Element_5.
Element_2 has_shape decagon.
Element_2 has_colour #D94D3D.
Element_2 has_position (281, 325).
Element_2 is_positioned_top-left_of Element_1.
Element_2 is_positioned_top-left_of Element_3.
Element_2 is_positioned_top_of Element_4.
Element_2 is_positioned_top_of Element_5.
Element_3 has_shape octagon.
Element_3 has_colour #290B54.
Element_3 has_position (6, 75).
Element_3 is_positioned_bottom-right_of Element_1.
Element_3 is_positioned_bottom-right_of Element_2.
Element_3 is_positioned_bottom-right_of Element_4.
Element_3 is_positioned_right_of Element_5.
Element_4 has_shape decagon.
Element_4 has_colour #C23B4F.
Element_4 has_position (271, 187).
Element_4 is_positioned_left_of Element_1.
Element_4 is_positioned_bottom_of Element_2.
Element_4 is_positioned_top-left_of Element_3.
Element_4 is_positioned_top_of Element_5.
Element_5 has_shape triangle.
Element_5 has_colour #F6FA95.
Element_5 has_position (226, 47).
Element_5 is_positioned_bottom-left_of Element_1.
Element_5 is_positioned_bottom_of Element_2.
Element_5 is_positioned_left_of Element_3.
Element_5 is_positioned_bottom_of Element_4.
    </pre></td>
  </tr>
</table>


## License
MIT License

Copyright (c) 2023 Simple Shapes Generator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
