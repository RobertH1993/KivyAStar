#!/bin/env python3


class AStarNode:
    def __init__(self, parent=None, position=None):
        self._parent = parent
        self._position = position

        self._f = 0
        self._g = 0
        self._h = 0

    @property
    def parent(self):
        return self._parent

    @property
    def position(self):
        return self._position

    @property
    def f_value(self):
        return self._f

    @f_value.setter
    def f_value(self, f):
        self._f = f

    @property
    def g_value(self):
        return self._g

    @g_value.setter
    def g_value(self, g):
        self._g = g

    @property
    def h_value(self):
        return self._h

    @h_value.setter
    def h_value(self, h):
        self._h = h

    def __eq__(self, other):
        return self._position == other.position

    def __repr__(self):
        return "POS: {}, F: {}, G: {}, H: {}".format(self._position, self._f, self._g, self._h)


class AStarRoute:
    def __init__(self, map):
        self._map = map

        self._open_list = []
        self._closed_list = []

    def start(self, start, end):
        self._open_list.append(AStarNode(None, start))
        while len(self._open_list) > 0:
            current_node = self._open_list[0]
            for node in self._open_list:
                if node.f_value < current_node.f_value:
                    current_node = node
            self._open_list.remove(current_node)

            # Check if route is found
            if current_node.position == end:
                return current_node
                break

            # Generate adjacent nodes
            for adjacent_relative_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                adjacent_position = (
                        current_node.position[0] + adjacent_relative_position[0],
                        current_node.position[1] + adjacent_relative_position[1]
                )

                # Check if adjacent is within map
                if adjacent_position[0] < 0 or adjacent_position[0] >= len(self._map):
                    continue
                elif adjacent_position[1] < 0 or adjacent_position[1] >= len(self._map[adjacent_position[0]]):
                    continue

                # Check if item is empty cell or start / stop cell
                if self._map[adjacent_position[0]][adjacent_position[1]] == GridField.WALL_PIXEL:
                    continue

                new_node = AStarNode(current_node,
                                     (adjacent_position[0], adjacent_position[1])
                                     )

                # Check if node already in closed list
                if new_node in self._closed_list:
                    continue

                # All okay, calc values and append to open list
                new_node.g_value = current_node.g_value + 1
                new_node.h_value = ((new_node.position[0] - end[0]) ** 2) + \
                                   ((new_node.position[1] - end[1]) ** 2)
                new_node.f_value = new_node.g_value + new_node.h_value

                # Check if node in open list with lower value
                for open_node in self._open_list:
                    if open_node == new_node and new_node.g_value > open_node.g_value:
                        continue

                self._open_list.append(new_node)
                self._closed_list.append(current_node)


from main import GridField

