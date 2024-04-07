import requests


url = "http://localhost:8000/"


#Crear paciente
ruta_post = url + "pacientes"
nuevo_paciente = {
    "ci": 7062817,
    "nombre": "Edwardd",
    "apellido": "Arias",
    "edad": 25,
    "genero": "Masculino",
    "diagnosticos": ["Diabetes", "Dolor de cabeza"],
    "doctor": "Pedro Perez"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print("Crear paciente", post_response.text)

#Listar pacientes

ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print("Listar pacientes", get_response.text)

#Buscar paciente por id

ruta_get_ci = url + "pacientes/7062816"
get_response = requests.request(method="GET", url=ruta_get_ci)
print("Buscar paciente por id", get_response.text)

#Listar paciente por diagnostico

ruta_get_diagnostico = url + "pacientes/?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get_diagnostico)
print("Listar paciente por diagnostico", get_response.text)

#Listar paciente por doctor

ruta_get_doctor = url + "pacientes/?doctor=Pedro Perez"
get_response = requests.request(method="GET", url=ruta_get_doctor)
print("Listar paciente por doctor", get_response.text)

#Actualizar paciente

ruta_update = url + "pacientes/7062817"
update_paciente = {
    "ci": 7062817,
    "nombre": "Edward",
    "edad": 21,
    "genero": "Masculino",
    "diagnosticos": ["Diabetes", "Resfriado"],
}
post_response = requests.request(method="PUT", url=ruta_update, json=update_paciente)
print("Actualizar paciente", post_response.text)

#Eliminar paciente

ruta_delete = url + "pacientes/7062817"
post_response = requests.request(method="DELETE", url=ruta_delete)
print("Eliminar paciente", post_response.text)
