
import random

def obter_localizacao_mock():
    return {
        "latitude": round(-23.74 + random.uniform(0.00, 0.13), 6),
        "longitude": round(-46.57 + random.uniform(0.00, 0.09), 6)
    }
