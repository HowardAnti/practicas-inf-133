from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import numpy as np
from urllib.parse import urlparse, parse_qs

partidas=[]

class Player:
    _instance = None

    def __new__(cls, name):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.name = name
            cls._instance.state = None
        return cls._instance
    
    def player_state(self):
        return self.state
    
    def define_player(self, state):
        self.state = state

            

    
class PlayerHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data        
    
    def server_state(self):
        state = np.random.uniform(0,1)
        if 0<=state and state<=1/3:
            state_server="piedra"
        elif 1/3<state and state<=2/3:
            state_server="papel"
        elif 2/3<state and state<=1:
            state_server="tijera"
        
        return state_server
    
    def winner(self, state_player, state_server):
        if state_player=="piedra" and state_server=="tijera":
            return "gano"
        elif state_player=="piedra" and state_server=="papel":
            return "perdio"
        elif state_player=="papel" and state_server=="piedra":
            return "gano"
        elif state_player=="papel" and state_server=="tijera":
            return "perdio"
        elif state_player=="tijera" and state_server=="papel":
            return "gano"
        elif state_player=="tijera" and state_server=="piedra":
            return "perdio"
        else:
            return "empate"
    
    def id_function(self):
        if partidas:
            return len(partidas)+1
        else:
            return 1
    
    def add_partida(self, player_state):
        server_state = self.server_state()
        partida = {
            "id": self.id_function(),
            "elemento": player_state,
            "elemento_servidor": server_state,
            "resultado": self.winner(player_state, server_state),
        }
        partidas.append(partida)
        return partida
        
    def filter_partidas(self, nombre, filter):
        return [partida for partida in partidas if partida["resultado"]==filter]
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == "/partidas" and not query_params:
            self.response_handler(200, partidas)
        elif "resultado" in query_params:
            resultado = query_params["resultado"][0]
            response_data = self.filter_partidas("resultado", resultado)
            self.response_handler(200, response_data)
        else:
            self.response_handler(404, {"Error":"Ruta no encontrada"})

    def do_POST(self):
        if self.path == "/partidas":
            data = self.read_data()
            player.define_player(data.get("elemento",None))
            response_data = self.add_partida(player.player_state())
            self.response_handler(201, [response_data])
        else:
            self.response_handler(404, {"Error":"Ruta no encontrada"})

def run_server():
    global player
    player = Player("Howard")
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PlayerHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()