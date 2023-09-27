import socketserver
import threading
from config import *
from logcolors import log, logOk, logEr, logW
import json
import time
from random import randint


MSG_ERROR = 'ERROR:'
MSG_WARNING = 'WARNING:'
MSG_OK = 'Ok:'


class PlayerId:
    IDs = [] 
    def __init__(self, len_players) -> None:
        self.Id = len_players
    
    def new_id(self, default=1):
        self.Id += default
        if self.Id not in self.IDs:
            self.IDs.append(self.Id)
            return self.Id
        else:
            return self.new_id(default + 1)
    
    @classmethod
    def del_id(cls, player):
        cls.IDs.remove(player.ID)


class Room:
    rooms = {}

    def __init__(self):
        self.name = str()
        self.players = dict()

    @staticmethod
    def create():
        room = Room()
        return room

    def __str__(self) -> str:
        return f'name: {self.name}\n players: {self.players}\nrooms: {self.rooms}, '
    
    @property
    def is_full(self):
        if len(self.players) > FULL_ROOM:
            return False
        return True
    
    def __len__(self):
        return len(self.players)

    def append(self, player):
        self.players[player.ID] = player
    
    def remove(self, player):
        if player.ID in self.players:
            self.players.pop(player.ID)
        else:
            logEr(MSG_ERROR, 'player not found in room')
            #------------------------------------------------------------

    def append_room(self, room):
        self.players[room.name] = room
    
    def remove_room(self, room):
        if room.name in self.players:
            self.players.pop(room.name)
        else:
            logEr(MSG_ERROR, 'player not found in room')
            #------------------------------------------------------------
    
    @classmethod
    def check(cls, name):
        if name in cls.rooms:
            return False
        return True
    

class Player:
    players = {}
    objID = PlayerId(len(players))

    def __init__(self, req):
        self.ID = self.objID.new_id()
        self.name = str()
        self.room_name = str()
        self.room = None
        self.req = req
        
        self.hand = list()
        self.score = 0
        
        self.lose_round = None
        self.lose_game = None
        
        self.is_move = None
        
        self.data = None

    @staticmethod
    def create_player(req):
        player = Player(req)
        player.players[player.ID] = player
        return player
    
    def __len__(self):
        return len(self.players)

    def get_data(self):
        data = self.req.recv(1024).decode()
        self.data = json.loads(data)

        if data:
            log('data of player:', data)
            #------------------------------------------------------------

        if "player_name" in self.data and "room_name" in self.data:
            self.name = self.data["player_name"]
            self.room_name = self.data["room_name"]
        else:
            self.get_data()
            logEr(MSG_ERROR, 'The expected data did not arrive')
            #------------------------------------------------------------

        if data:
            return data

    def send_message(self, message):
        try:
            client_socket = self.req
            client_socket.sendall(json.dumps(message).encode())
            logOk(f'Send message:', f'{message}')
            #------------------------------------------------------------
        except:
            logEr(MSG_ERROR, 'message did not send')
            #------------------------------------------------------------

    @classmethod
    def append(cls, player):
        cls.players[player.ID] = player

    @classmethod
    def remove(cls, player):
        cls.players.pop(player.ID)
    
    @staticmethod
    def login_room(req):
        player = Player.create_player(req)
        player.get_data()
        if player.name and player.room_name:
            if Room.check(player.room_name):
                room = Room.create()
                room.name = player.room_name
                room.rooms[room.name] = room
                room.append(player)
                player.room = room
                player.append(player)
            else:
                player.room = Room.rooms[player.room_name]
                player.room.append(player)
                player.append(player)
        print('ROOM:', Room.rooms[player.room_name])
        player.send_message({'room_status': '200'})
        if Room.check(player.room_name):
            return player, room
        
        return player, Room.rooms[player.room_name]

    
    def logging(self):
        logOk(
            'logging ',
            f'amount players in {self.players} is: {self.name}' 
        )
        #--------------------------------------------------------
        logOk('logging ', f'amount rooms is: {self.room.rooms}')
        #--------------------------------------------------------

    def disconnect(self, player, room):
        logW('Disconnected:', {self.name})
        message = {
            "event": "player_disconnect",
            "player_name": self.name
        }
        if not Room.check(self.room_name):
            self.remove(player)
            self.room.remove(player)
            if len(room) < 1:
                Room.rooms.pop(self.room_name)
        else:
            self.remove(player)
            self.room.remove(player)
        
        self.send_message(message)

        self.req.close()
        logOk("Ok!")


class CardGameHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logW('Connected', self.client_address)
        #--------------------------------------------------------

        player, room = Player.login_room(req=self.request)

        print(self.request)

        while True:
            try:
                data_player = player.get_data()
                if not data_player:
                    print('non data')
                    break
                else:
                    log('DATA:', f"{data_player}")
                    print(player.room)
                    #--------------------------------------------------------  
            except Exception as e:
                logW(MSG_WARNING, e)
                break

        player.disconnect(player, player.room)

        print('ROOM:', player.room)

        time.sleep(0.5)
        

def main_server():
    server = socketserver.ThreadingTCPServer((HOST, PORT), CardGameHandler)
    logOk("Server started on", f"{HOST}, {PORT}")
    #------------------------------------------------------------------------------

    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        try:
            server_thread.join()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main_server()
