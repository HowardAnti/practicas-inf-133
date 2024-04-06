import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}

# POST /deliveries
new_animal_data = {
    "tipo_animal": "anfibio",
    "nombre": "Federico",
    "especie": "Sapito",
    "genero": "Macho",
    "edad": 2,
    "peso": 1, 
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())

new_animal_data = {
    "tipo_animal": "mamifero",
    "nombre": "Pedro",
    "especie": "Monito",
    "genero": "Macho",
    "edad": 5,
    "peso": 5, 
}

response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())


# GET /deliveries
response = requests.get(url=url)
print(response.json())

# PUT /deliveries/{vehicle_id}
animal_id_to_update = 1
updated_animal_data = {
    "edad": 10,
    "peso": 7, 
}
response = requests.put(f"{url}/{animal_id_to_update}", json=updated_animal_data)
print("Animal actualizado:", response.json())

# GET /deliveries
response = requests.get(url=url)
print(response.json())

genero_get="?genero=Macho"

response = requests.get(f"{url}/{genero_get}")
print(response.json())

especie_get="?especie=Sapito"

response = requests.get(f"{url}/{especie_get}")
print(response.json())

# DELETE /deliveries/{vehicle_id}
animal_id_to_delete = 1
response = requests.delete(f"{url}/{animal_id_to_delete}")
print("Animal eliminado:", response.json())

# GET /deliveries
response = requests.get(url=url)
print(response.json())