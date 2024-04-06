import requests

url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}

# GET /pizzas
response = requests.get(url)
print(response.json())

# POST /pizzas 
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
print(response.json())

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

response = requests.get(url)
print(response.json())

response = requests.get(url + "/7062816")
print(response.json())

edit_paciente = {
    "edad": 24,
    "diagnosticos": ["Resfriado", "Diabetes"]
}
response = requests.put(url+"/7062816", json=edit_paciente, headers=headers)
print(response.json())

response = requests.get(url)
print(response.json())

doctor_searched="Pedro Perez"
response = requests.get(f"{url}/?doctor={doctor_searched}")
print(response.json())

diagnostico_searched="Diabetes"
response = requests.get(f"{url}/?diagnostico={diagnostico_searched}")
print("Diabetes", response.json())

response = requests.delete(url + "/7062816")
print(response.json())

# GET /pizzas
response = requests.get(url)
print(response.json())