from ui.layout import Layout
from pygame import Rect
from typing import Tuple

class VerticalLayout(Layout):
    def __init__(self, rect: Rect, spacing: int = 10, margins: Tuple[int, int, int, int] = (0, 0, 0, 0)) -> None:
        super().__init__(rect, margins)
        self.spacing = spacing

    def update_layout(self) -> None:
        y_offset = self.rect.top + self.margins[0]
        widget_height = (self.rect.height - self.margins[0] - self.margins[2] - (len(self.widgets) - 1) * self.spacing) // len(self.widgets)

        for widget in self.widgets:
            widget.set_dimensions((self.rect.width - self.margins[1] - self.margins[3], widget_height))
            self.set_position(widget, (self.rect.left + self.margins[3], y_offset))
            y_offset += widget_height + self.spacing