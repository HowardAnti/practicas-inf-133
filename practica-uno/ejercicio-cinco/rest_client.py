import requests


url = "http://localhost:8000/"


# Crear animal

ruta_post = url + "animales"
nuevo_animal = {
    "nombre": "Richard",
    "especie": "Tigre",
    "genero": "Macho",
    "edad": 5,
    "peso": 15,
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print("Crear animal", post_response.text)

#Listar animales

ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print("Listar animales", get_response.text)

#Buscar animales por especie

ruta_get_especie = url + "animales/?especie=Gato"
get_response = requests.request(method="GET", url=ruta_get_especie)
print("Buscar animales por especie", get_response.text)

#Buscar animales por genero

ruta_get_genero = url + "pacientes/?genero=Macho"
get_response = requests.request(method="GET", url=ruta_get_genero)
print("Buscar animales por genero", get_response.text)

#Actualizar animal

ruta_update = url + "animales/2"
update_animal = {
    "edad": 10,
    "peso": 25,
}
post_response = requests.request(method="PUT", url=ruta_update, json=update_animal)
print("Actualizar animal", post_response.text)

#Eliminar animal

ruta_delete = url + "animales/2"
post_response = requests.request(method="DELETE", url=ruta_delete)
print("Eliminar mensaje", post_response.text)
