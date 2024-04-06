from zeep import Client

client = Client('http://localhost:8000')

result = client.service.Suma(numberA=10, numberB=5)
print(result)

result = client.service.Resta(numberA=10, numberB=5)
print(result)

result = client.service.Multiplicacion(numberA=10, numberB=5)
print(result)

result = client.service.Division(numberA=10, numberB=5)
print(result)