
import random

def buscar_dados_ambientais(localizacao):
    return {
        "vegetacao": random.choice(["Suburbio", "Periferia", "Centro", "Zona Industrial", "Zona Rural"]),
        "temperatura": random.randint(12, 30),
        "umidade": random.randint(10, 55),
        "vento": random.randint(5, 30)
    }
