from ui.layout import Layout
from pygame import Rect
from typing import Tuple

class VerticalLayout(Layout):
    def __init__(self, relative_rect: Rect, 
                 manager, 
                 spacing: int = 0, 
                 margins: Tuple[int, int, int, int] = (0, 0, 0, 0), container=None) -> None:
        super().__init__(relative_rect, manager, spacing, margins, container=container)

    def update_layout(self) -> None:
        if len(self.elements) > 0:
            available_height = self.get_relative_rect().height - self.margins[0] - self.margins[2]
            y_offset = self.margins[0]
            widget_height = (available_height - (len(self.elements) - 1) * self.spacing) // len(self.elements)
            widget_width = self.get_relative_rect().width - self.margins[1] - self.margins[3]

            for widget in self.elements:
                widget.set_dimensions((widget_width, widget_height))
                widget.set_relative_position((self.margins[3], y_offset))
                if isinstance(widget, Layout):
                    widget.update_layout()
                y_offset += widget_height + self.spacing