import requests

url = "http://localhost:8000/"

#Crear mensaje

ruta_post = url + "mensajes"
nuevo_mensaje = {
    "contenido" : "Howard"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_mensaje)
print("Nuevo mensaje", post_response.text)

nuevo_mensaje = {
    "contenido" : "Hello, world!"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_mensaje)
print("Nuevo mensaje", post_response.text)

#Listar mensajes

ruta_get = url + "mensajes"
get_response = requests.request(method="GET", url=ruta_get)
print("Listar mensajes", get_response.text)

#Buscar mensajes por id

ruta_get_id = url + "mensajes/1"
get_response = requests.request(method="GET", url=ruta_get_id)
print("Buscar mensajes por id",  get_response.text)

#Actualizar mensajes

ruta_update = url + "mensajes/1"
update_mensaje = {
    "contenido" : "How you doing?"
}

post_response = requests.request(method="PUT", url=ruta_update, json=update_mensaje)
print("Actualizar mensajes", post_response.text)

#Eliminar mensajes

ruta_delete = url + "mensajes/1"
post_response = requests.request(method="DELETE", url=ruta_delete)
print("Eliminar mensaje", post_response.text)
