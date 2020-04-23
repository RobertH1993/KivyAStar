#!/bin/env python3
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window

from AStar import AStarRoute

import random


class GridField(Widget):
    EMPTY_PIXEL = 0
    WALL_PIXEL = 1
    START_PIXEL = 2
    END_PIXEL = 3
    PATH_PIXEL = 4

    def __init__(self):
        super(GridField, self).__init__()
        self._grid = []
        self._grid_needs_update = True
        self._start_position = None
        self._end_position = None

        # Config
        self._n_pixels = 60

        # Dynamic
        self._pixel_width = 0
        self._pixel_height = 0

        # Init the grid
        self._randomize_grid()

        # Request keyboard inputs
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _randomize_grid(self):
        self._grid = []
        for x in range(0, self._n_pixels):
            self._grid.append([])
            for y in range(0, self._n_pixels):
                self._grid[x].append(random.choice([GridField.WALL_PIXEL, GridField.EMPTY_PIXEL, GridField.EMPTY_PIXEL]))

        self._start_position = (
            random.randrange(0, self._n_pixels),
            random.randrange(0, self._n_pixels)
        )
        self._end_position = (
            random.randrange(0, self._n_pixels),
            random.randrange(0, self._n_pixels)
        )

        self._grid[self._start_position[0]][self._start_position[1]] = GridField.START_PIXEL
        self._grid[self._end_position[0]][self._end_position[1]] = GridField.END_PIXEL

    def _draw_pixel(self, x, y):
        with self.canvas:
            pixel_type = self._grid[x][y]
            if pixel_type == GridField.EMPTY_PIXEL:
                Color(1, 1, 1)
            elif pixel_type == GridField.WALL_PIXEL:
                Color(0, 0, 0)
            elif pixel_type == GridField.START_PIXEL:
                Color(0, 255, 0)
            elif pixel_type == GridField.END_PIXEL:
                Color(255, 0, 0)
            elif pixel_type == GridField.PATH_PIXEL:
                Color(1, 1, 0)
            else:
                raise ValueError("Invalid pixel type: ", pixel_type)

            Rectangle(pos=(self._pixel_width*x, self._pixel_height*y),
                      size=(self._pixel_width, self._pixel_height)
                      )

    def _draw_grid(self):
        self._pixel_width = int(self.width / self._n_pixels)
        self._pixel_height = int(self.height / self._n_pixels)

        print("Pixel h: {}, w: {}".format(self._pixel_height, self._pixel_width))

        for x in range(0, self._n_pixels):
            for y in range(0, self._n_pixels):
                self._draw_pixel(x, y)

    def update_pixel(self, x, y, pixel_type):
        if x >= self._n_pixels or y >= self._n_pixels:
            raise ValueError("X or Y position bigger then n_pixels")
        self._grid[x][y] = pixel_type
        self._draw_pixel(x, y)

    def on_touch_down(self, touch):
        x, y = touch.pos

        # Convert coordinates to pixel
        x = int(x / self._pixel_width)
        y = int(y / self._pixel_height)

        # Update pixel type
        pixel_type = not self._grid[x][y]
        self.update_pixel(x, y, pixel_type)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'r':
            self._randomize_grid()
            self._grid_needs_update = True
        if keycode[1] == 's':
            print("Got start")
            route = AStarRoute(self._grid)
            end_node = route.start(self._start_position, self._end_position)
            if not end_node:
                print("No route to end!")
                return

            current_node = end_node
            while current_node.parent:
                current_node = current_node.parent
                self.update_pixel(current_node.position[0],
                                  current_node.position[1],
                                  GridField.PATH_PIXEL)

    def update(self, dt):
        if self._grid_needs_update:
            self._draw_grid()
            self._grid_needs_update = False


class AStar(App):
    def build(self):

        game = GridField()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    AStar().run()
