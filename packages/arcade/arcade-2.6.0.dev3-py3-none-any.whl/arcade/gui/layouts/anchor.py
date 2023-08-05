from typing import Union

from arcade import Sprite
from arcade.gui import UIElement
from arcade.gui.layouts import UILayout


class UIAnchorLayout(UILayout):
    """

    Layout which places its children according to two anchor values
    (bottom|top and left|right).

    Supported pack options:
    - top|bottom: anchor on y axis
    - left|right: anchor on x axis
    - fill_x: fill x axis
    - fill_y: fill y axis

    """

    # TODO add parameters to init with viewport values
    def __init__(self, width, height, **kwargs):
        super().__init__(size_hint=(1.0, 1.0), **kwargs)

        self._width = width
        self._height = height

    def place_elements(self):
        # FIXME do not overdraw others!

        for element, data in self._elements:
            element: Union[UILayout, UIElement, Sprite]
            top = data.get("top")
            left = data.get("left")
            bottom = data.get("bottom")
            right = data.get("right")
            center_x = data.get("center_x")
            center_y = data.get("center_y")

            fill_x = data.get("fill_x")
            fill_y = data.get("fill_y")

            min_size = getattr(element, "min_size", None)
            size_hint = getattr(element, "size_hint", None)
            if min_size or size_hint:
                # one is set, so we are allowed to change elements size

                # use current element size, if no min_size was provided
                min_width, min_height = min_size or (element.width, element.height)
                hint_width, hint_height = size_hint or (0, 0)

                width = max(min_width, int(hint_width * self.width))
                height = max(min_height, int(hint_height * self.height))

                element.width = width
                element.height = height

            # legacy pack kwargs
            if fill_x:
                element.width = self._width
            if fill_y:
                element.height = self._height

            if bottom is not None:
                element.bottom = self.bottom + bottom
            elif top is not None:
                element.top = self.top - top
            elif center_y is not None:
                element.center_y = self.center_y + center_y

            if left is not None:
                element.left = self.left + left
            elif right is not None:
                element.right = self.right - right
            elif center_x is not None:
                element.center_x = self.center_x + center_x
