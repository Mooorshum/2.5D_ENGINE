from typing import Tuple
from pygame import Rect
from pygame_gui.core import UIContainer, IContainerLikeInterface
from pygame_gui import UIManager

class Layout(UIContainer):
    def __init__(self, relative_rect: Rect,
                 manager: UIManager,
                 spacing: int,
                 margins: Tuple[int, int, int, int] = (0, 0, 0, 0), 
                 container : IContainerLikeInterface = None) -> None:
        super().__init__(relative_rect=relative_rect, manager=manager, container=container)
        self.margins = margins
        self.spacing = spacing

    def add_element(self, element: IContainerLikeInterface) -> None:
        super().add_element(element)
        self.update_layout()

    def update_layout(self) -> None:
        pass
