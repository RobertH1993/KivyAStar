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
    def __init__(self, map, start, end, field=None):
        self._map = map
        self._start = start
        self._end = end
        self._field = field

        self._open_list = []
        self._open_list.append(AStarNode(None, self._start))
        self._closed_list = []

    def step(self):
        if len(self._open_list) > 0:
            current_node = self._open_list[0]
            for node in self._open_list:
                if node.f_value < current_node.f_value:
                    current_node = node
            self._open_list.remove(current_node)
            self._closed_list.append(current_node)

            self._field.update_pixel(current_node.position[0],
                                     current_node.position[1],
                                     GridField.CLOSED_NODE_PIXEL)


            # Check if route is found
            if current_node.position == self._end:
                return current_node

            # Generate adjacent nodes
            adjacent_nodes = []
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
                adjacent_nodes.append(new_node)

            # Walk through adjacent nodes
            for adjacent_node in adjacent_nodes:
                break_loop = False
                for closed_node in self._closed_list:
                    if adjacent_node == closed_node:
                        break_loop = True
                        break

                if break_loop:
                    continue

                # All okay, calc values and append to open list
                adjacent_node.g_value = current_node.g_value + 1
                adjacent_node.h_value = ((adjacent_node.position[0] - self._end[0]) ** 2) + \
                                        ((adjacent_node.position[1] - self._end[1]) ** 2)
                adjacent_node.f_value = adjacent_node.g_value + adjacent_node.h_value

                # Check if node in open list with lower value
                for open_node in self._open_list:
                    if open_node == adjacent_node:
                        break_loop = True
                        if adjacent_node.g_value > open_node.g_value:
                            break
                        else:
                            self._open_list.remove(open_node)
                            self._open_list.append(adjacent_node)
                if break_loop:
                    continue

                # Draw open node if needed
                if self._field:
                    self._field.update_pixel(adjacent_node.position[0],
                                            adjacent_node.position[1],
                                            GridField.OPEN_NODE_PIXEL)

                self._open_list.append(adjacent_node)


from main import GridField


