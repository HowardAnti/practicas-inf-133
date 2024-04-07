import requests

url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}


# Crear paciente 

mi_paciente = {
    "ci": 7062816,
    "nombre": "Howard",
    "apellido": "Anti",
    "edad": 21,
    "genero": "Masculino",
    "diagnosticos": ["Resfriado", "Dolor de cabeza", "Diabetes"],
    "doctor": "Gregory House"
}
response = requests.post(url, json=mi_paciente, headers=headers)
print("Crear paciente", response.json())

mi_paciente = {
    "ci": 7062817,
    "nombre": "Briana",
    "apellido": "Arias",
    "edad": 27,
    "genero": "Feminino",
    "diagnosticos": ["Diabetes"],
    "doctor": "Pedro Perez"
}
response = requests.post(url, json=mi_paciente, headers=headers)
print(response.json())

#Listar pacientes

response = requests.get(url)
print("Listar pacientes", response.json())

#Buscar pacientes por ci

response = requests.get(url + "/7062816")
print("Buscar paciente por ci", response.json())

#Listar por diagnostico

diagnostico_searched="Diabetes"
response = requests.get(f"{url}/?diagnostico={diagnostico_searched}")
print("Listar por diagnostico", response.json())

#Listar por doctor

doctor_searched="Pedro Perez"
response = requests.get(f"{url}/?doctor={doctor_searched}")
print("Listar por doctor", response.json())

#Actualizar paciente

edit_paciente = {
    "edad": 24,
    "diagnosticos": ["Resfriado", "Diabetes"]
}
response = requests.put(url+"/7062816", json=edit_paciente, headers=headers)
print("Actualizar paciente", response.json())

#Eliminar paciente

response = requests.delete(url + "/7062816")
print("Eliminar paciente", response.json())

