import math
import random
from typing import Dict, List, Any

import yaml
import svgwrite
from svgwrite.container import Group


def random_choice(options):
    return random.choice(options)


def parse_canvas_size(size_str):
    width, height = size_str.split("x")
    return int(width), int(height)


def parse_yaml() -> Any:
    with open("parameters.yaml", "r") as file:
        params = yaml.safe_load(file)
    return params


def parse_components() -> Dict:
    params = parse_yaml()
    components = {}
    for key, value in params["element_defs"].items():
        components[key] = create_component(value)
    return components


# draw_component draws the center elements and children for the PolygonGroup
def draw_component(dwg, center, center_element):
    components = parse_components()
    component = components[center_element]
    size_option = random_choice(component.style["size_options"])
    rotation_option = random_choice(component.style["rotation_options"])
    return component.draw(dwg, center, size_option, rotation_option)


class Component:
    def __init__(self, id, style):
        self.id = id
        self.style = style

    def draw(self, dwg, center, size, rotation):
        pass


class Circle(Component):
    def draw(self, dwg, center, size, rotation):
        circle = dwg.circle(
            center=center,
            r=size / 2,
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )
        return circle


class Rect(Component):
    def draw(self, dwg, center, size, rotation):
        x, y = center
        rect = dwg.rect(
            insert=(x - size / 2, y - size / 2),
            size=(size, size),
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )
        if rotation != 0:
            rect.rotate(rotation, center)
        return rect


class Ellipse(Component):
    def draw(self, dwg, center, size, rotation):
        ellipse = dwg.ellipse(
            center=center,
            r=(size / 2, size / 4),
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )
        if rotation != 0:
            ellipse.rotate(rotation, center)
        return ellipse


class Polygon(Component):
    def __init__(self, id: str, style: Dict, vertex_count: List, center_elements: List):
        super().__init__(id, style)
        self.vertex_count = random_choice(vertex_count)
        self.center_element = random_choice(center_elements)

    def draw(self, dwg, center, size, rotation):
        x, y = center
        p = (0, size * 0.5)
        points_list = [p, ]

        for i in range(self.vertex_count):
            p = self._rotate(p, (360 / self.vertex_count) * (math.pi / 180))
            points_list.append(p)
        points_list = [(i[0] + x, i[1] + y) for i in points_list]

        polygon = dwg.polygon(
            points=points_list,
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )
        if rotation != 0:
            polygon.rotate(rotation, center)
        if self.center_element is None:
            return polygon

        center_component = draw_component(dwg, center, self.center_element)
        group_components = Group()
        group_components.add(polygon)
        group_components.add(center_component)
        return group_components

    @staticmethod
    def _rotate(p, angle):
        return (round(p[0] * math.cos(-angle) - p[1] * math.sin(-angle), 7),
                round(p[0] * math.sin(-angle) + p[1] * math.cos(-angle), 7))
    

class PolygonGroup(Component):
    def __init__(self, id: str, style: Dict, vertex_count: List, vertex_elements: List, center_elements: List):
        super().__init__(id, style)
        self.vertex_count = random_choice(vertex_count)
        self.vertex_elements = random_choice(vertex_elements)
        self.center_element = random_choice(center_elements)

    def draw(self, dwg, center, size, rotation):
        x, y = center
        p = (0, size * 0.5)
        points_list = [p, ]

        for i in range(self.vertex_count):
            p = self._rotate(p, (360 / self.vertex_count) * (math.pi / 180))
            points_list.append(p)
        points_list = [(i[0] + x, i[1] + y) for i in points_list]

        polygon = dwg.polygon(
            points=points_list,
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )

        group_components = Group()
        group_components.add(polygon)

        if self.center_element is not None:
            center_component = draw_component(dwg, center, self.center_element)
            group_components.add(center_component)

        match self.vertex_elements:
            case "circle":
                for i in range(self.vertex_count):
                    child_component = draw_component(dwg, points_list[i], "circle")
                    group_components.add(child_component)
            case "polygon":
                for i in range(self.vertex_count):
                    child_component = self.draw_child_polygon(dwg, points_list[i], size, rotation)
                    group_components.add(child_component)
        return group_components

    # draw_child_polygon draws a child polygon
    def draw_child_polygon(self, dwg, center, size, rotation):
        x, y = center
        p = (0, size * 0.5)
        points_list = [p, ]

        for i in range(self.vertex_count):
            p = self._rotate(p, (360 / self.vertex_count) * (math.pi / 180))
            points_list.append(p)
        points_list = [(i[0] + x, i[1] + y) for i in points_list]

        polygon = dwg.polygon(
            points=points_list,
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )
        if rotation != 0:
            polygon.rotate(rotation, center)
        return polygon

    @staticmethod
    def _rotate(p, angle):
        return (round(p[0] * math.cos(-angle) - p[1] * math.sin(-angle), 7),
                round(p[0] * math.sin(-angle) + p[1] * math.cos(-angle), 7))


# Create instances of the components based on the YAML parameters
def create_component(params):
    component_type = params["type"]
    style = params["style"]

    if component_type == "Circle":
        return Circle(params["id"], style)
    elif component_type == "Rect":
        return Rect(params["id"], style)
    elif component_type == "Ellipse":
        return Ellipse(params["id"], style)
    elif component_type == "Polygon":
        return Polygon(params["id"], style, params["vertex_count"], params["center_elements"])
    elif component_type == "PolygonGroup":
        return PolygonGroup(
            params["id"],
            style,
            params["vertex_count_options"],
            params["vertex_elements"],
            params["center_elements"]
        )


def main():
    params = parse_yaml()
    components = parse_components()

    # Create the SVG drawing
    canvas_width, canvas_height = parse_canvas_size(params["canvas_size"])
    dwg = svgwrite.Drawing("output.svg", size=(canvas_width, canvas_height))

    # Draw the requested components
    for component_id in params["component_to_draw"]:
        component = components[component_id]

        center_option = (canvas_width / 2, canvas_height / 2)
        size_option = random_choice(component.style["size_options"])
        rotation_option = random_choice(component.style["rotation_options"])

        element = component.draw(dwg, center_option, size_option, rotation_option)
        dwg.add(element)

    # Save the SVG file
    dwg.save()


if __name__ == '__main__':
    main()
