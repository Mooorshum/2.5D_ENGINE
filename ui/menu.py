from typing import Tuple

from pygame import Rect, QUIT
import pygame.event as evt

from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIPanel, UIButton

from ui import START_GAME_EVENT
from ui.vertical_layout import VerticalLayout



class MainMenu:
    def __init__(self, size : Tuple[int, int]) -> None:
        
        self.manager = UIManager(size, 'ui/styles.json')
        panel_width = int(size[0] / 4)
        panel_height = int(size[1] / 4)
        display_rect = Rect((size[0]/2 - panel_width/2, size[1]/2 - panel_height/2), (panel_width, panel_height))
        self.layout = VerticalLayout(display_rect, self.manager, spacing=10, margins=(10,10,10,10))

        self.start_button = UIButton(
            relative_rect=Rect((0, 0), (20, 20)),
            text='Start Game',
            manager=self.manager,
            container=self.layout
        )

        self.preferences_button = UIButton(
            relative_rect=Rect((0, 0), (20, 20)),
            text='Preferences',
            manager=self.manager,
            container=self.layout
        )

        self.exit_button = UIButton(
            relative_rect=Rect((0, 0), (20, 20)),
            text='Exit',
            manager=self.manager,
            container=self.layout
        )

        
    def hide(self) -> None:
        self.layout.hide()

    def show(self) -> None:
        self.layout.show()

    def process_events(self, event) -> None:
        self.manager.process_events(event)
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                evt.post(evt.Event(START_GAME_EVENT))
            elif event.ui_element == self.exit_button:
                evt.post(evt.Event(QUIT))

    def is_visible(self) -> bool:
        return self.layout.visible

    def draw(self, screen, time_delta) -> None:
        if self.layout.visible:
            self.manager.update(time_delta)
            self.manager.draw_ui(screen)

