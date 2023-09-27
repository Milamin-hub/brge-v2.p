import pygame
import pygame_menu
from window import main_game
from config import SCREEN_WIDTH, SCREEN_HEIGHT, HOST, PORT
import socket
import threading
import requests
import json


pygame.init()
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption('Bridge')

#-----------------------------------------------------------------------------------------

class User:
    
    def __init__(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_thread = threading.Thread(
            target=self.receive_messages
        )
        self.server_address = (HOST, PORT)
        self.is_con = None
        self.is_inet = None
        self.player_name = None
        self.room_name = None
        self.is_action = False

    def connect_to_server(self):
        self.check_internet_connection()
        if self.is_inet:
            try:
                self.client_socket.connect(self.server_address)
                self.is_con = True
                print("Successfully connected to the server.")
            except ConnectionRefusedError:
                self.is_con = False
                print("Error: An error occurred while connecting to the server.")
            except Exception as e:
                self.is_con = False
                print(f"An error occurred while connecting to the server: {str(e)}")

    def check_internet_connection(self):
        try:
            response = requests.get("http://www.google.com", timeout=5)
            response.raise_for_status()
            self.is_inet = True
        except requests.exceptions.RequestException:
            self.is_inet = False
            print("Error: Check your internet connection.")

    def send_data(self, data):
        if self.is_con:
            self.client_socket.sendall(json.dumps(data).encode())
            print('Data sent successfully', data)
        else:
            print('Error: Connection to server not received...')

    def send_name_and_room(self):
        if self.player_name and self.room_name:
            data = {"player_name": self.player_name, 'room_name': self.room_name}
            self.send_data(data)
            print('Sending data to server: ok')
        else:
            print('Error: Data not sent')

    def receive_messages(self):
        # Получить данные от сервера
        try:
            self.data = self.client_socket.recv(1024).decode()
            if not self.data:
                self.is_action = False
            print('data:',self.data)
            if self.data:
                data_dict = json.loads(self.data)
                if data_dict["room_status"] == "200":
                    self.is_action = True
                else:
                    self.is_action = False
        except Exception as e:
            print("Error: Error processing message from server")

    def run_tread(self):
        try:
            self.receive_thread.daemon = True
            self.receive_thread.start()
        except Exception as e:
            print("Error: Error with threads")

    def disconnect_from_server(self):
        try:
            self.client_socket.close()
            print("The connection to the server is closed.")
        except Exception as e:
            print(f"Error when closing connection to server: {str(e)}")


class Menu:
    input_data = {}
    user = User()
    user.connect_to_server()
    user.run_tread()

    def __init__(self, surface) -> None:
        self.WINDOW_SIZE = WINDOW_SIZE
        self.surface = surface
        self.is_run = True
        self.data = None
        self.is_action = False

        # Тема с темным фоном для главного меню
        self.main_menu_theme = pygame_menu.themes.Theme(
            background_color=(30, 30, 30),
            title_font_size=30
        )
        self.main_menu = pygame_menu.Menu(
            height=self.WINDOW_SIZE[1] * 0.7,
            onclose=pygame_menu.events.EXIT,
            theme=self.main_menu_theme,
            title='Menu',
            width=self.WINDOW_SIZE[0] * 0.8,
        )

    @classmethod
    def re_connect(cls):
        cls.user = User()
        cls.user.connect_to_server()
        cls.user.run_tread()

    def data_of_input(self, value, input_name, action):
        self.input_data[input_name] = value
        print(self.input_data)
        if action is not None:
            if value:
                if input_name == 'name':
                    self.user.player_name = value
                    action()
                elif input_name == 'room':
                    self.user.room_name = value   

                    if self.user.room_name and self.user.player_name:
                        self.user.send_name_and_room()

                        if self.user.is_action:
                            action()
    
    def add_button(self, title, action=None):
        self.main_menu.add.button(title, action)

    def add_label(self, text):
        label = self.main_menu.add.label(text)
        label.set_position(-10, 50)

    def add_input(self, title='Name: ', name='name', action=None):
        self.main_menu.add.text_input(
            title,
            default=self.input_data[name] if name in self.input_data else '',
            onreturn=lambda value: self.data_of_input(value, name, action),
            maxchar=10,
        )
    
    def menu_loop(self):
        pygame.time.delay(100)
        self.main_menu.mainloop(self.surface)

    def menu_disable(self):
        self.main_menu.disable()


class UIMenu:

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.menu = Menu(self.screen)
    
    def new_menu(self):
        self.menu = Menu(self.screen)

    def menu_create_room(self, back_menu=None):
        self.check_back_menu(back_menu)

        self.menu.add_input(title='Room: ', name='room', action=lambda: self.enter_room(self.menu))
        self.menu.add_button('Back', lambda: self.menu_rooms(self.menu))

        self.menu.menu_loop()

    def check_back_menu(self, back_menu):
        if back_menu:
            back_menu.menu_disable()
        
        self.new_menu()

    def menu_rooms(self, back_menu=None):
        self.check_back_menu(back_menu)

        self.menu.add_button('Enter the room', lambda: self.menu_create_room(self.menu))
        self.menu.add_button('Back', lambda: self.main_menu(self.menu))

        self.menu.menu_loop()


    def main_menu(self, back_menu=None, re_con=False) -> None:
        self.check_back_menu(back_menu)

        if re_con:
            self.menu.user.disconnect_from_server()
            self.menu.re_connect()
            re_con = False

        if self.menu.user.is_con:
            self.menu.add_label('Enter a name and press Enter')
            self.menu.add_input(name='name', action=lambda: self.menu_rooms(self.menu))
        else:
            self.menu.add_label("Error: I can not connect to server")

        self.menu.menu_loop()

    def exit_menu(self, back_menu=None):
        self.check_back_menu(back_menu)

        self.menu.user.disconnect_from_server()
        self.menu.menu_disable()

    def out_or_menu(self, back_menu=None):
        self.check_back_menu(back_menu)

        self.menu.add_button('Exit', lambda: self.exit_menu(self.menu))
        self.menu.add_button('Menu', lambda: self.main_menu(re_con=True))

        self.menu.menu_loop()


    def enter_room(self, back_menu=None):
        self.check_back_menu(back_menu)

        if self.menu.user.is_action:
            main_game()
            self.out_or_menu()

#-----------------------------------------------------------------------------------------


if __name__ == '__main__':
    main = UIMenu()
    main.main_menu()