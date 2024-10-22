from ui.layout import Layout
from pygame import Rect
from typing import Tuple

class VerticalLayout(Layout):
    def __init__(self, relative_rect: Rect, manager, spacing: int = 10, margins: Tuple[int, int, int, int] = (0, 0, 0, 0)) -> None:
        super().__init__(relative_rect, manager, margins)
        self.spacing = spacing

    def update_layout(self) -> None:
        if len(self.elements) > 0:
            available_height = self.rect.height - self.margins[0] - self.margins[2]
            y_offset = self.rect.top + self.margins[0]
            widget_height = (available_height - (len(self.elements) - 1) * self.spacing) // len(self.elements)
            print(widget_height, available_height, len(self.elements))
            for widget in self.elements:
                widget.set_dimensions((self.get_relative_rect().width - self.margins[1] - self.margins[3], widget_height))
                self.set_position(widget, (self.get_relative_rect().left + self.margins[3], y_offset))
                y_offset += widget_height + self.spacing