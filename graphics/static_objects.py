from graphics.sprite_stacks import SpritestackModel

class Building(SpritestackModel):
    def __init__(self, type=None, name=None, scale=1):
        super().__init__(type, name, scale)

        self.rotation = 0