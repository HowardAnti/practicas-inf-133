import requests

url = "http://localhost:8000/partidas"



# Crear partidas

player_state={
    "elemento": "piedra"
}

response = requests.request(
    method="POST", url=url, json=player_state
)
print("Crear partida: ", response.text)

player_state={
    "elemento": "papel"
}

response = requests.request(
    method="POST", url=url, json=player_state
)
print("Crear partida: ", response.text)

player_state={
    "elemento": "tijera"
}

response = requests.request(
    method="POST", url=url, json=player_state
)
print("Crear partida: ", response.text)


# Listas partidas

response = requests.request(method="GET", url=url)
print("Listar partidas", response.text)

# Listar partidas perdidas 

response = requests.request(
    method="GET", url=url + "?resultado=perdio", json=player_state
)
print("Partidas perdidas", response.text)

# Listar partidas ganadas

response = requests.request(
    method="GET", url=url + "?resultado=gano", json=player_state
)
print("Partidas ganadas", response.text)