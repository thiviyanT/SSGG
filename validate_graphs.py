import re
import sys


def validate_knowledge_graph(knowledge_graph: str) -> bool:
    lines = knowledge_graph.strip().split('\n')

    element_pattern = r"element_\d+"
    shape_pattern = r"[a-zA-Z0-9_]+"
    position_pattern = r"\(\d+,\s*\d+\)"
    color_pattern = r"[a-zA-Z0-9_]+"
    direction_pattern = r"left|right|above|below|top_left|top_right|bottom_left|bottom_right"

    shape_statement = re.compile(f"^{element_pattern} has_shape {shape_pattern}$")
    position_statement = re.compile(f"^{element_pattern} has_position {position_pattern}$")
    color_statement = re.compile(f"^{element_pattern} has_colour {color_pattern}$")
    relative_position_statement = re.compile(f"^{element_pattern} is_positioned_{direction_pattern}_of {element_pattern}$")

    for line in lines:
        if shape_statement.match(line):
            continue
        elif position_statement.match(line):
            continue
        elif color_statement.match(line):
            continue
        elif relative_position_statement.match(line):
            continue
        else:
            print(f"Invalid statement: {line}")
            return False

    return True


if __name__ == "__main__":
    # Read the knowledge graph from a file or use a sample string
    with open("knowledge_graph.txt", "r") as file:
        knowledge_graph = file.read()

    is_valid = validate_knowledge_graph(knowledge_graph)

    if is_valid:
        print("The knowledge graph is semantically valid.")
    else:
        print("The knowledge graph is not semantically valid.")
