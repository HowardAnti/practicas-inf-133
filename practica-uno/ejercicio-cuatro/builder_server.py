from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from urllib.parse import urlparse, parse_qs

pacientes = {}

class Paciente:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnosticos = []
        self.doctor = None

    def __str__(self):
        return f"ci: {self.ci}, Nombre: {self.nombre}, Apellido: {self.apellido}, Edad: {self.edad},Genero: {self.genero}, Diagnosticos: {', '.join(self.diagnosticos)}, Doctor: {self.doctor}"

class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()

    def set_ci(self, ci):
        self.paciente.ci = ci

    def set_nombre(self, nombre):
        self.paciente.nombre = nombre

    def set_apellido(self, apellido):
        self.paciente.apellido = apellido
    
    def set_edad(self, edad):
        self.paciente.edad = edad
        
    def set_genero(self, genero):
        self.paciente.genero = genero

    def add_diagnosticos(self, diagnostico):
        self.paciente.diagnosticos.append(diagnostico)
    
    def set_doctor(self, doctor):
        self.paciente.doctor = doctor

    def get_paciente(self):
        return self.paciente


class Hospital:
    def __init__(self, builder):
        self.builder = builder

    def create_paciente(self, ci, nombre, apellido, edad, genero, diagnosticos, doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        for diagnostico in diagnosticos:
            self.builder.add_diagnosticos(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()


# Aplicando el principio de responsabilidad única (S de SOLID)
class HospitalService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)

    def create_paciente(self, post_data):
        ci = post_data.get("ci", None)
        nombre = post_data.get("nombre", None)
        apellido = post_data.get("apellido", None)
        edad = post_data.get("edad", None)
        genero = post_data.get("genero", None)
        diagnosticos = post_data.get("diagnosticos", [])
        doctor = post_data.get("doctor", None)

        paciente = self.hospital.create_paciente(ci, nombre, apellido, edad, genero, diagnosticos, doctor)
        
        if pacientes:
            id=max(pacientes.keys())+1
        else:
            id=1
        
        pacientes[id] = paciente
        
        return paciente

    def read_pacientes(self):
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}
    
    def read_paciente(self, ci):
        for index in pacientes:
            paciente = pacientes[index]
            if paciente.ci == ci:
                return paciente    
        return None
    
    def filter_paciente(self, nombre, tipo):
        filter_pacientes={index: paciente.__dict__ for index, paciente in pacientes.items() if paciente.__dict__[f"{nombre}"]==tipo}
        if filter_pacientes:
            return filter_pacientes
        else:
            return None
    
    def filter_diagnostico(self, diagnostico_searched):
        filter_pacientes={index: paciente.__dict__ for index, paciente in pacientes.items() 
                          for diagnostico in paciente.__dict__["diagnosticos"]
                          if diagnostico == diagnostico_searched}
        if filter_pacientes:
            return filter_pacientes
        else:
            return None
    
    def update_paciente(self, ci, data):
        for index in pacientes:
            paciente = pacientes[index]
            if paciente.ci == ci:
                nombre = data.get("nombre", None)
                apellido = data.get("apellido", None)
                edad = data.get("edad", None)
                genero = data.get("genero", None)
                diagnosticos = data.get("diagnosticos", [])
                doctor = data.get("doctor", None)
                
                if nombre:
                    paciente.nombre = nombre
                if apellido:
                    paciente.apellido = apellido
                if edad:
                    paciente.edad = edad
                if genero:
                    paciente.genero = genero
                if diagnosticos:
                    paciente.diagnosticos = diagnosticos
                if doctor:
                    paciente.doctor = doctor
                

                return paciente
        
        return None

    def delete_paciente(self, ci):
        for index in pacientes:
            paciente = pacientes[index]
            if paciente.ci == ci:
                pacientes.pop(index)
                return paciente    
        return None


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))
        

# Manejador de solicitudes HTTP
class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = HospitalService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_paciente(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == "/pacientes":
            response_data = self.controller.read_pacientes()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif self.path.startswith("/pacientes/") and not query_params:
            ci = int(self.path.split("/")[2])
            response_data = self.controller.read_paciente(ci)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        elif "doctor" in query_params:
            doctor = query_params["doctor"][0]
            response_data = self.controller.filter_paciente("doctor", doctor)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 202, {"message": f"ningun paciente es atendido por {doctor}"})
        elif "diagnostico" in query_params:
            diagnostico = query_params["diagnostico"][0]
            response_data = self.controller.filter_diagnostico(diagnostico)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 202, {"message": f"ningun paciente fue diagnosticado con {diagnostico}"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_paciente(ci, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de paciente no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[2])
            deleted_paciente = self.controller.delete_paciente(ci)
            if deleted_paciente:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Paciente eliminado correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de paciente no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    try:
        server_address = ("", port)
        httpd = server_class(server_address, handler_class)
        print(f"Iniciando servidor HTTP en puerto {port}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor...")
        httpd.socket.close()


if __name__ == "__main__":
    run()