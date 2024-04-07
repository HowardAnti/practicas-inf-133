import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}

# Crear animal tipo anfibio
new_animal_data = {
    "tipo_animal": "anfibio",
    "nombre": "Federico",
    "especie": "Sapito",
    "genero": "Macho",
    "edad": 2,
    "peso": 1, 
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print("Crear animal:", response.json())

# Crear animal tipo mamifero

new_animal_data = {
    "tipo_animal": "mamifero",
    "nombre": "Pedro",
    "especie": "Monito",
    "genero": "Macho",
    "edad": 5,
    "peso": 5, 
}

response = requests.post(url=url, json=new_animal_data, headers=headers)
print("Crear animal:", response.json())

# Listar animales

response = requests.get(url=url)
print("Listar animales:", response.json())

#Buscar animales por especie

especie_get="?especie=Sapito"

response = requests.get(f"{url}/{especie_get}")
print("Buscar por especie:", response.json())

#Buscar animales por genero

genero_get="?genero=Macho"

response = requests.get(f"{url}/{genero_get}")
print("Buscar por genero:", response.json())

# Actualizar animal

animal_id_to_update = 1
updated_animal_data = {
    "edad": 10,
    "peso": 7, 
}
response = requests.put(f"{url}/{animal_id_to_update}", json=updated_animal_data)
print("Actualizar animal:", response.json())

# Eliminar animal

animal_id_to_delete = 1
response = requests.delete(f"{url}/{animal_id_to_delete}")
print("Eliminar animal:", response.json())
