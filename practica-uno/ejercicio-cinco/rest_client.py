import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los estudiantes por la ruta /estudiantes
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
# POST agrega un nuevo estudiante por la ruta /estudiantes
ruta_post = url + "animales"
nuevo_animal = {
    "nombre": "Richard",
    "especie": "Tigre",
    "genero": "Macho",
    "edad": 5,
    "peso": 15,
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print(post_response.text)

ruta_update = url + "animales/2"
update_animal = {
    "edad": 10,
    "peso": 25,
}
post_response = requests.request(method="PUT", url=ruta_update, json=update_animal)
print(post_response.text)

ruta_get_especie = url + "animales/?especie=Gato"
get_response = requests.request(method="GET", url=ruta_get_especie)
print(get_response.text)

ruta_get_genero = url + "pacientes/?genero=Macho"
get_response = requests.request(method="GET", url=ruta_get_genero)
print(get_response.text)



ruta_delete = url + "animales/2"
post_response = requests.request(method="DELETE", url=ruta_delete)
print(post_response.text)
# GET filtrando por nombre con query params
#ruta_get = url + "estudiantes?nombre=Pedrito"
#get_response = requests.request(method="GET", url=ruta_get)
#print(get_response.text)