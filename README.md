# Тестовое задание на генератор

## Дано

Есть базовый генератор, который на основе схемы, описанной в `parameters.yaml` генерирует SVG

В генераторе реализованы отдельные геометрические фигуры и прямоугольная сетка 

## Задача

Необходимо реализовать два новых компонента:

* Полигон - элемент с заданым количеством вершин
* Полигональная группа - компонент наподобие сетки, который расставляет дочерние элементы в вершинах полигона
Количество вершин задаётся в конфиге. Отдельно указываются центральные элементы


## Пример плолигона
![Полигон](./polygon.png)

## Пример полигональной группы
![Полигональная группа](./polygon-group.png)

## Целевой конфиг
```yaml

canvas_size: 30x30

element_defs:

  background:
    type: Rect
    id: background
    center_elements: [null]
    style:
      fill_options: [white]
      opacity_options: [1.0]
      size_options: [30]
      rotation_options: [0]

  circle:
    type: Circle
    id: circle
    center_elements: [null, rect]
    style:
      fill_options: [red, green]
      opacity_options: [0.25, 0.5, 0.75, 1.0]
      size_options: [5]#, 10, 15, 20]
      rotation_options: [0, 90, 180, 270]

  polygon:
    type: Polygon
    id: polygon
    vertex_count: [3, 4, 5]
    center_elements: [null, rect]
    style:
      fill_options: [purple, yellow]
      opacity_options: [0.25, 0.5, 0.75, 1.0]
      size_options: [5]#, 10, 15, 20]
      rotation_options: [0, 90, 180, 270]

  polygon_group:
    type: PolygonGroup
    id: polygon_group
    vertex_count_options: [5]#3, 4, 6, 8]
    vertex_elements: [circle, polygon]
    center_elements: [null, polygon]
    style:
      fill_options: [red, green]
      opacity_options: [0.25, 0.5, 0.75, 1.0]
      size_options: [5]#, 10, 15, 20]
      rotation_options: [0, 90, 180, 270]
      stroke: [red, green]
      stroke_width: [1, 2]

component_to_draw: [background, polygon_group]
```
