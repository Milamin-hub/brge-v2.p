import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, MAX_SCORE
from UIButton import ButtonMicroPhone, ButtonSound, ButtonMenu


pygame.init()
pygame.display.set_caption('Bridge')


class Window:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.is_run = True

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            self.is_run = False

    def quit_window(self):
        self.is_run = False

    def render(self):
        pygame.display.flip()

# -------------------------------------------------------------------------------------------

class Card:
    _window = Window()

    def __init__(self, suit: str, rank: int, is_back: bool=True) -> None:
        self.suit = suit
        self.rank = rank
        self.card_path = f'cards/{self.suit}{self.rank}.png'
        self.is_back = is_back
        self.__size = (60, 85)
        self.__load = self.load_card()
        self.rect = self.__load.get_rect()

    def load_card(self):
        if not self.is_back:
            self.card_path = f'cards/{self.suit}{self.rank}.png'
        else:
            self.card_path = f'cards/BackCard.png'
        self.card_load = pygame.image.load(self.card_path)
        self.__load = pygame.transform.scale(self.card_load, self.__size)
        return self.__load

    def draw(self, pos):
        self._window.screen.blit(self.__load, pos)

    def rotate_card(self):
        if self.is_back:
            self.is_back = False
        else:
            self.is_back = True
        self.load_card()

    @property
    def size(self):
        return self.__size

# -------------------------------------------------------------------------------------------

class Deck:
    def __init__(self) -> None:
        self.cards = []
        self.dragging_card = None
        self.dragging_offset = (0, 0)
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for rank in range(6, 15):
                card = Card(suit, rank)
                card.rect.x = SCREEN_WIDTH // 1.5 - card.size[0] * 1.1
                card.rect.y = SCREEN_HEIGHT // 2 - card.size[1] // 1.5
                self.cards.append(card)
        random.shuffle(self.cards)

# -------------------------------------------------------------------------------------------

class Player:
    def __init__(self) -> None:
        self.name = None
        self.cards = []
        self.score = 0
        self.is_move = False
        self.is_active = False
        self.is_lose = True
        self.dragging_card = None
        self.dragging_offset = (0, 0)
    
    def take_card(self, deck):
        if self.score < MAX_SCORE: 
            card = deck.cards.pop()
            card.rotate_card()
            self.cards.append(card)

        elif self.score == MAX_SCORE:
            self.score = 0
        else:
            self.is_lose = True
    
    def pl_move(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Search for the top card under the mouse
                for card in reversed(self.cards):
                    if card.rect.collidepoint(event.pos):
                        self.is_move = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_move = False

    def pl_cards_pos(self):
        if not self.is_move:
            for i, card in enumerate(reversed(self.cards)):
                if card.rect[1] < SCREEN_HEIGHT - card.size[1] - 100:
                    card.rect[1] = SCREEN_HEIGHT - card.size[1] - 10
                    card.rect[0] -= 40 * i
                elif card.rect[1] > SCREEN_HEIGHT - card.size[1] - 100:
                    card.rect[1] = SCREEN_HEIGHT - card.size[1] - 10

    
# -------------------------------------------------------------------------------------------

class Croupier:
    def __init__(self) -> None:
        self.deck = Deck()

    def move_card(self, event, obj):
        # obj is Deck or Player or cards of Broken
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Search for the top card under the mouse
                for card in reversed(obj.cards):
                    if card.rect.collidepoint(event.pos):
                        top_card = card
                        obj.dragging_card = top_card
                        obj.dragging_offset = (
                            card.rect.centerx - event.pos[0],
                            card.rect.centery - event.pos[1]
                        )
                        obj.cards.remove(top_card)
                        obj.cards.append(top_card)
                        break

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and obj.dragging_card is not None:
                # Возвращение карты в исходное положение
                obj.dragging_card.rect.centerx = event.pos[0]
                obj.dragging_card.rect.centery = event.pos[1]
                obj.dragging_card = None
        
        if obj.dragging_card is not None:
            # Перемещение карты за мышью
            obj.dragging_card.rect.centerx, obj.dragging_card.rect.centery = pygame.mouse.get_pos()
    
    def show_cards(self, obj):
        for card in obj.cards:
            card.draw((card.rect.x, card.rect.y))

# -------------------------------------------------------------------------------------------

class Game:
    def __init__(self) -> None:
        self.is_end_round = False
        self.is_end_game = True

    def start_round(self):
        pass

    def end_round(self):
        pass

    def start_game(self):
        pass

    def end_game(self):
        pass

# -------------------------------------------------------------------------------------------

def main_game():
    window = Window()
    deck = Deck()
    player = Player()
    croupier = Croupier()
    micro = ButtonMicroPhone()
    sound = ButtonSound()
    menu = ButtonMenu()

    micro.x = SCREEN_WIDTH - 40
    micro.y = SCREEN_HEIGHT // 2 - 55
    micro.load()

    sound.x = SCREEN_WIDTH - 40
    sound.y = SCREEN_HEIGHT // 2
    sound.load()

    menu.x = SCREEN_WIDTH - 40
    menu.load()
    

    for i in range(3):
        player.take_card(deck)

    while window.is_run:

        window.screen.fill((30, 30, 30))

        for event in pygame.event.get():
            window.event_handler(event)

            player.pl_move(event)

            croupier.move_card(event, player)

            micro.action(event)
            sound.action(event)
            menu.action(event)

        player.pl_cards_pos()

        croupier.show_cards(player)
        croupier.show_cards(deck)

        micro.update(window.screen)
        sound.update(window.screen)
        menu.update(window.screen)

        window.render()


if __name__ == '__main__':
    main_game()