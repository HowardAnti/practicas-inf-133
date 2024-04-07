import requests

url = 'http://localhost:8000/graphql'

#Activar venv con zeep y graphene
#Crear planta

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
print("Crear planta:", response_mutation.text)

#Listar plantas

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
print("Listar plantas:", response.text)

#Buscar plantas por especie

query = """
    {
        plantaPorEspecie(especie: "Orquidea"){
            nombre
        }
    }
"""


response = requests.post(url, json={'query': query})
print("Plantas por especie:", response.text)

#Buscar plantas que tienen frutos

query_frutos = """
    {
        frutos{
            nombre
        }
    }
"""

response = requests.post(url, json={'query': query_frutos})
print("Buscar por frutos:", response.text)

#Actualizar planta

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
print("Actualizar planta:", response.text)

#Eliminar planta

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
print("Eliminar planta:", response_mutation.text)


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
print("Listar plantas:", response.text)