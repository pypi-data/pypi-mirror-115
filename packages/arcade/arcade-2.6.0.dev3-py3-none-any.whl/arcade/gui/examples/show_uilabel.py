import arcade

import arcade.gui
from arcade.gui import UIManager


class MyView(arcade.View):
    def __init__(self, my_window: arcade.Window):
        super().__init__(my_window)

        self.ui_manager = UIManager(self.window)

    def on_draw(self):
        arcade.start_render()
        self.ui_manager.on_draw()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.ui_manager.purge_ui_elements()
        self.ui_manager.enable()

        self.ui_manager.add_ui_element(
            arcade.gui.UILabel(
                text="Hello world",
                center_x=self.window.width // 2,
                center_y=self.window.height // 2,
            )
        )

    def on_hide_view(self):
        self.ui_manager.disable()


if __name__ == "__main__":
    window = arcade.Window(title="ARCADE_GUI")
    window.show_view(MyView(window))
    arcade.run()
