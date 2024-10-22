from typing import Tuple

from pygame import Rect, QUIT
import pygame.event as evt

from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UIButton
from pygame_gui import UI_BUTTON_PRESSED

from ui import START_GAME_EVENT
from ui.vertical_layout import VerticalLayout



class MainMenu:
    def __init__(self, size : Tuple[int, int]) -> None:
        
        self.manager = UIManager(size, 'ui/styles.json')
        panel_width = int(size[0] / 4)
        panel_height = int(size[1] / 4)
        self.panel = UIPanel(
            relative_rect=Rect((size[0]/2 - panel_width/2, size[1]/2 - panel_height/2), (panel_width, panel_height)),
            starting_height=1,
            manager=self.manager,
        
        )

        self.layout = VerticalLayout(self.panel.get_relative_rect(), spacing=10, margins=(10,10,10,10))
        
        self.start_button = UIButton(
            relative_rect=Rect((0, 0), (20, 20)),
            text='Start Game',
            manager=self.manager,
            container=self.panel
        )

        self.layout.add_widget(self.start_button)

        self.preferences_button = UIButton(
            relative_rect=Rect((0, 0), (20, 20)),
            text='Preferences',
            manager=self.manager,
            container=self.panel
        )

        self.layout.add_widget(self.preferences_button)

        self.exit_button = UIButton(
            relative_rect=Rect((0, 0), (20, 20)),
            text='Exit',
            manager=self.manager,
            container=self.panel
        )

        self.layout.add_widget(self.exit_button)
        
    def hide(self) -> None:
        self.panel.hide()

    def show(self) -> None:
        self.panel.show()

    def process_events(self, event) -> None:
        self.manager.process_events(event)
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                evt.post(evt.Event(START_GAME_EVENT))
            elif event.ui_element == self.exit_button:
                evt.post(evt.Event(QUIT))

    def is_visible(self) -> bool:
        return self.panel.visible

    def draw(self, screen, time_delta) -> None:
        if self.panel.visible:
            self.manager.update(time_delta)
            self.manager.draw_ui(screen)

