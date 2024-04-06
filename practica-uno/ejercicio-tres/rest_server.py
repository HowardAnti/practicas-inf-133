from http.server import HTTPServer, BaseHTTPRequestHandler
import json


from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci": 7062816,
        "nombre": "Howard",
        "apellido": "Anti",
        "edad": 21,
        "genero": "Masculino",
        "diagnosticos": ["Resfriado", "Dolor de cabeza"],
        "doctor": "Gregory House",
        "id": 1
    }
]


class RESTRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def find_paciente(self, ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"] == ci),
            None,
        )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        
        if parsed_path.path == "/pacientes":
            self.response_handler(200, pacientes)
        elif parsed_path.path.startswith("/pacientes/") and not query_params:
            ci=int(parsed_path.path.split("/")[-1])
            paciente=self.find_paciente(ci)
            self.response_handler(200, [paciente])
        elif "diagnostico" in query_params:
            diagnostico_tipo = query_params["diagnostico"][0]
            pacientes_filtrados = [
                    paciente
                    for paciente in pacientes
                    for diagnostico in paciente["diagnosticos"]
                    if diagnostico == diagnostico_tipo
                ]
            if pacientes_filtrados != []:
                self.response_handler(200, pacientes_filtrados)
            else:
                self.response_handler(204, [])
        elif "doctor" in query_params:
            doctor = query_params["doctor"][0]
            pacientes_filtrados = [
                paciente
                for paciente in pacientes
                    if paciente["doctor"] == doctor
                ]
            if pacientes_filtrados != []:
                self.response_handler(200, pacientes_filtrados)
            else:
                self.response_handler(204, [])
                

        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            data["id"] = len(pacientes) + 1
            pacientes.append(data)
            self.response_handler(201, pacientes)

        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            estudiante = self.find_paciente(ci)
            data = self.read_data()
            if estudiante:
                estudiante.update(data)
                self.response_handler(200, pacientes)
            else:
                self.response_handler(404, {"Error": "Estudiante no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente_delete=self.find_paciente(ci)
            if paciente_delete:
                pacientes.remove(paciente_delete)    
                self.response_handler(200, pacientes)
            else:
                self.response_handler(404, {"Error": "Estudiante no encontrado"})
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