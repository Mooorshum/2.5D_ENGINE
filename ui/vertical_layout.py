from ui.layout import Layout
from pygame import Rect
from typing import Tuple

class VerticalLayout(Layout):
    def __init__(self, relative_rect: Rect, manager, spacing: int = 0, margins: Tuple[int, int, int, int] = (0, 0, 0, 0)) -> None:
        super().__init__(relative_rect, manager, margins)
        self.spacing = spacing

    def update_layout(self) -> None:
        if len(self.elements) > 0:
            available_height = self.get_relative_rect().height - self.margins[0] - self.margins[2]
            y_offset = self.margins[0]
            widget_height = (available_height - (len(self.elements) - 1) * self.spacing) // len(self.elements)
            for widget in self.elements:
                if isinstance(widget, Layout):

                    widget.set_dimensions((self.get_relative_rect().width - self.margins[1] - self.margins[3], widget_height))
                    widget.set_relative_position((self.get_relative_rect().left + self.margins[3],
                                                  self.get_relative_rect().top + y_offset))
                    widget.update_layout()
                else:
                    widget.set_dimensions((self.get_relative_rect().width - self.margins[1] - self.margins[3], widget_height))
                    widget.set_relative_position((self.margins[3], y_offset))
                y_offset += widget_height + self.spacing