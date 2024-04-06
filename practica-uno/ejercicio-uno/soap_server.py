from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def suma(numberA, numberB):
    return numberA+numberB

def resta(numberA, numberB):
    return numberA-numberB

def multiplicacion(numberA, numberB):
    return numberA*numberB

def division(numberA, numberB):
    return (numberA+0.0)/numberB

dispatcher = SoapDispatcher(
    "operaciones-soap-server",
    location="http://localhost:8000",
    action="http://localhost:8000",
    namespace="http://localhost:8000",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Suma",
    suma,
    returns={"suma": int},
    args={"numberA": int, "numberB":int}
)

dispatcher.register_function(
    "Resta",
    resta,
    returns={"resta": int},
    args={"numberA": int, "numberB":int}
)

dispatcher.register_function(
    "Multiplicacion",
    multiplicacion,
    returns={"multiplicacion": int},
    args={"numberA": int, "numberB":int}
)

dispatcher.register_function(
    "Division",
    division,
    returns={"division": float},
    args={"numberA": int, "numberB": int}
)

def run():
    try:
        server=HTTPServer(("0.0.0.0", 8000), SOAPHandler)
        server.dispatcher = dispatcher
        print("Servidor SOAP iniciado en http://localhost:8000/")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Apagando Servidor SOAP")
        server.socket.close()
        
if __name__=="__main__":
    run()