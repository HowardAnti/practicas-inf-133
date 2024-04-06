import requests

url = 'http://localhost:8000/graphql'


query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""

response = requests.post(url, json={'query': query_lista})
print(response.text)


query = """
    {
        plantaPorEspecie(especie: "Orquidea"){
            nombre
        }
    }
"""


response = requests.post(url, json={'query': query})
print(response.text)


query_crear = """
mutation {
        crearPlanta(nombre: "Genesis", especie: "Girasol", edad: 12, altura: 15, frutos: false) {
            planta {
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

query_frutos = """
    {
        frutos{
            nombre
        }
    }
"""


response = requests.post(url, json={'query': query_frutos})
print(response.text)

query_update = """
mutation {
        updatePlanta(id: 1, nombre="Gen", especie="fdsa", edad: 3, altura: 21, frutos: false){
            planta{
                especie
            }
        }
}

"""

response = requests.post(url, json={'query': query_update})
print(response.text)

query_eliminar = """
mutation {
        deletePlanta(id: 2) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query_lista})
print(response.text)