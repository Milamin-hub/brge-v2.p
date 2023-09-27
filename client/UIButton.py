import pygame


class ExButton:
    backgroung = (30, 30, 30)

    def __init__(self) -> None:
        self.is_on = False
        self.button_width = 35 
        self.button_height = 35
        self.button_load = None
        self.button_rect = None
        self.x = 0
        self.y = 0
        self.path = None

    def load(self):
        self.button_load = pygame.image.load(self.path)
        self.rect()
    
    def rect(self):
        if self.button_load:
            self.button_load = pygame.transform.scale(
                self.button_load, (
                    self.button_width,
                    self.button_height
                )
            )
            self.button_rect = self.button_load.get_rect()

    def action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.change()

    def change(self):
        self.is_on = not self.is_on
        self.load()

    def update(self, screen):
        self.button_rect.x = self.x
        self.button_rect.y = self.y
        screen.blit(self.button_load, self.button_rect)


class ButtonMicroPhone(ExButton):
    def __init__(self) -> None:
        super().__init__()

    def load(self):
        if self.is_on:
            self.path = 'buttons/micro/on.svg'
        else:
            self.path = 'buttons/micro/off.svg'
        super().load()


class ButtonSound(ExButton):
    def __init__(self) -> None:
        super().__init__()
        self.is_on = True

    def load(self):
        if self.is_on:
            self.path = 'buttons/sound/on.svg'
        else:
            self.path = 'buttons/sound/off.svg'
        super().load()


class ButtonMenu(ExButton):
    def __init__(self) -> None:
        super().__init__()
        self.is_on = True

    def load(self):
        if self.is_on:
            self.path = 'buttons/menu/on.svg'
        else:
            self.path = 'buttons/menu/back.svg'
        super().load()


if __name__ == "__main__":
    # screen = pygame.display.set_mode((800, 600))
    # micro = MicroPhone()
    # micro.x = 255
    # micro.load()
    # while True:
    #     ...
    #     for event in pygame.event.get():
    #         ...
    #         micro.action(event)

    #     micro.update(screen)
    print('Hello World!')


