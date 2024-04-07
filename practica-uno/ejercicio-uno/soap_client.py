from zeep import Client

client = Client('http://localhost:8000')

#Se necesita activar el venv
#Suma

result = client.service.Suma(numberA=10, numberB=5)
print("Suma", result)

#Resta

result = client.service.Resta(numberA=10, numberB=5)
print("Resta", result)

#Multiplicacion

result = client.service.Multiplicacion(numberA=10, numberB=5)
print("Multiplicacion", result)

#Division

result = client.service.Division(numberA=10, numberB=5)
print("Division",result)