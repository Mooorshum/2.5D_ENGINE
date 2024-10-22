from ui.layout import Layout
from pygame import Rect
from typing import Tuple

class HorizontalLayout(Layout):
    def __init__(self, relative_rect: Rect, manager, spacing: int = 0, margins: Tuple[int, int, int, int] = (0, 0, 0, 0)) -> None:
        super().__init__(relative_rect, manager, margins)
        self.spacing = spacing

    def update_layout(self) -> None:
        if len(self.elements) > 0:
            available_width = self.get_relative_rect().width - self.margins[1] - self.margins[3]
            x_offset = self.margins[3]  # Начинаем с левого отступа
            widget_width = (available_width - (len(self.elements) - 1) * self.spacing) // len(self.elements)

            for widget in self.elements:
                widget_height = self.get_relative_rect().height - self.margins[0] - self.margins[2]
                widget_rect = Rect(
                    (x_offset, self.margins[0]),  # Отступы слева и сверху
                    (widget_width, widget_height)
                )

                # Устанавливаем относительную позицию независимо от типа
                widget.set_relative_position((x_offset, self.margins[0]))
                widget.set_dimensions((widget_width, widget_height))

                # Если это вложенный лэйаут, обновляем его
                if isinstance(widget, Layout):
                    widget.update_layout()  # Обновляем расположение вложенного лэйаута

                x_offset += widget_width + self.spacing