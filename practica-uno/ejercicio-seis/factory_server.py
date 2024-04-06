from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

animales = {}


class Animal:
    def __init__(self, tipo_animal, nombre, especie, genero, edad, peso):
        self.tipo_animal = tipo_animal
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso


class Mamifero(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("mamifero", nombre, especie, genero, edad, peso)
        
class Ave(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("ave", nombre, especie, genero, edad, peso)

class Reptil(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("reptil", nombre, especie, genero, edad, peso)

class Anfibio(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("anfibio", nombre, especie, genero, edad, peso)
        
class Pez(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("pez", nombre, especie, genero, edad, peso)



class ZoologicoFactory:
    @staticmethod
    def create_animal(tipo_animal, nombre, especie, genero, edad, peso):
        if tipo_animal == "mamifero":
            return Mamifero(nombre, especie, genero, edad, peso)
        elif tipo_animal == "ave":
            return Ave(nombre, especie, genero, edad, peso)
        elif tipo_animal == "reptil":
            return Reptil(nombre, especie, genero, edad, peso)
        elif tipo_animal == "anfibio":
            return Anfibio(nombre, especie, genero, edad, peso)
        elif tipo_animal == "pez":
            return Pez(nombre, especie, genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no válido")


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


class ZoologicoService:
    def __init__(self):
        self.factory = ZoologicoFactory()

    def add_animal(self, data):
        tipo_animal = data.get("tipo_animal", None)
        nombre = data.get("nombre", None)
        especie = data.get("especie", None)
        genero = data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)

        animal = self.factory.create_animal(
            tipo_animal, nombre, especie, genero, edad, peso
        )
        if animales:
            id=max(animales.keys())+1
        else:
            id=1
        animales[id] = animal
        return animal

    def list_animales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}

    def list_filter(self, nombre,filter):
        animales_filtrados={index: animal.__dict__ for index, animal in animales.items() if animal.__dict__[f"{nombre}"]==filter}
        if animales_filtrados:
            return animales_filtrados
        else:
            raise None
    
    def update_animal(self, animal_id, data):
        if animal_id in animales:
            animal = animales[animal_id]
            nombre = data.get("nombre", None)
            especie = data.get("especie", None)
            genero = data.get("genero", None)
            edad = data.get("edad", None)
            peso = data.get("peso", None)
            if nombre:
                animal.nombre=nombre
            if especie:
                animal.especie=especie
            if genero:
                animal.genero=genero
            if edad:
                animal.edad=edad
            if peso:
                animal.peso=peso
                
            return animal
        else:
            raise None

    def delete_animal(self, animal_id):
        if animal_id in animales:
            del animales[animal_id]
            return {"message": "Animal eliminado"}
        else:
            return None


class ZoologicoRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.zoologico_service = ZoologicoService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoologico_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == "/animales":
            response_data = self.zoologico_service.list_animales()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif "genero" in query_params:
            genero = query_params["genero"][0]
            response_data = self.zoologico_service.list_filter("genero",genero)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Especie no encontrada"})
        elif "especie" in query_params:
            especie = query_params["especie"][0]
            response_data = self.zoologico_service.list_filter("especie",especie)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Especie no encontrada"})
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoologico_service.update_animal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.zoologico_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ZoologicoRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()