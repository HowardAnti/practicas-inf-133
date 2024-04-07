from http.server import HTTPServer, BaseHTTPRequestHandler
import json


mensajes = []


class RESTRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def find_mensaje(self, id):
        return next(
            (mensaje for mensaje in mensajes if mensaje["id"] == id),
            None,
        )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def cesar(self, mensaje, shift):
        encrypted_message = ""
        for char in mensaje:
            if char.isalpha():
                ascii_code = ord(char)
                if char.isupper():
                    encrypted_ascii_code = (ascii_code - ord('A') + shift) % 26 + ord('A')
                else:
                    encrypted_ascii_code = (ascii_code - ord('a') + shift) % 26 + ord('a')
                encrypted_char = chr(encrypted_ascii_code)
                encrypted_message += encrypted_char
            else:
                encrypted_message += char
        return encrypted_message
    
    def add_encripted_message(self, contenido):
        encripted_message={
            "contenido": contenido,
            "contenido encriptado": self.cesar(contenido,3),
            "id": len(mensajes)+1
        }
        mensajes.append(encripted_message)
        return encripted_message

    def updated_cesar(self, mensaje, data):
        mensaje["contenido"] = data.get("contenido", None)
        mensaje["contenido encriptado"] = self.cesar(data.get("contenido", None),3)
    
    def do_GET(self):
        
        if self.path == "/mensajes":
            self.response_handler(200, mensajes)
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje_filtrado = self.find_mensaje(id)
            if mensaje_filtrado:
                self.response_handler(200, [mensaje_filtrado])
            else:
                self.response_handler(404, {"Error": "Mensaje no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            response_data = self.add_encripted_message(data.get("contenido", None))
            self.response_handler(201, [response_data])

        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = self.find_mensaje(id)
            data = self.read_data()
            if mensaje:
                self.updated_cesar(mensaje, data)
                self.response_handler(200, mensajes)
            else:
                self.response_handler(404, {"Error": "Mensaje no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje_delete=self.find_mensaje(id)
            if mensaje_delete:
                mensajes.remove(mensaje_delete)    
                self.response_handler(200, mensajes)
            else:
                self.response_handler(404, {"Error": "Mensaje no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})
        


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()