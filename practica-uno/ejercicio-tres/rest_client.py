import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los estudiantes por la ruta /estudiantes
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
# POST agrega un nuevo estudiante por la ruta /estudiantes
ruta_post = url + "pacientes"
nuevo_paciente = {
    "ci": 7062817,
    "nombre": "Edwardd",
    "apellido": "Arias",
    "edad": 25,
    "genero": "Masculino",
    "diagnostico": ["Diabetes", "Dolor de cabeza"],
    "doctor": "Pedro Perez"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)

ruta_update = url + "pacientes/7062817"
update_paciente = {
    "ci": 7062817,
    "nombre": "Edward",
    "edad": 21,
    "genero": "Masculino",
    "diagnosticos": ["Diabetes", "Resfriado"],
}
post_response = requests.request(method="PUT", url=ruta_update, json=update_paciente)
print(post_response.text)

ruta_get_ci = url + "pacientes/7062816"
get_response = requests.request(method="GET", url=ruta_get_ci)
print(get_response.text)

ruta_get_diagnostico = url + "pacientes/?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get_diagnostico)
print(get_response.text)

ruta_get_doctor = url + "pacientes/?doctor=Pedro Perez"
get_response = requests.request(method="GET", url=ruta_get_doctor)
print(get_response.text)



ruta_delete = url + "pacientes/7062817"
post_response = requests.request(method="DELETE", url=ruta_delete)
print(post_response.text)
# GET filtrando por nombre con query params
#ruta_get = url + "estudiantes?nombre=Pedrito"
#get_response = requests.request(method="GET", url=ruta_get)
#print(get_response.text)