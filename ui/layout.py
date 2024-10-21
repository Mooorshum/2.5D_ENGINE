from typing import Tuple
from pygame import Rect

class Layout:
    def __init__(self, rect: Rect, margins: Tuple[int, int, int, int] = (0, 0, 0, 0)) -> None:
        self.rect = rect
        self.widgets = []
        self.margins = margins

    def add_widget(self, widget) -> None:
        self.widgets.append(widget)
        self.update_layout()

    def update_layout(self) -> None:
        pass

    def set_position(self, widget, position: Tuple[int, int]) -> None:
        widget.set_position(position)
