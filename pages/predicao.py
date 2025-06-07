
def prever_propagacao(temp, umidade, vento, vegetacao):
    import streamlit as st

    risco = (temp * 0.4 + vento * 0.4) - (umidade * 0.2)
    if vegetacao == "Zona Rural":
        risco *= 1.5
    elif vegetacao == "Zona Industrial":
        risco *= 1.25
    elif vegetacao == "Centro":
        risco *= 1.2
    elif vegetacao == "Periferia":
        risco *= 1.1
    elif vegetacao == "Suburbio":
        risco *= 1.05


    risco = round(max(risco, 0), 2)

    if risco < 30:
        nivel = "baixo"
    elif risco < 60:
        nivel = "moderado"
    else:
        nivel = "elevado"

    if vento > 20:
        direcao = "norte"
    elif vento > 10:
        direcao = "nordeste"
    else:
        direcao = "leste"

    resposta = f"""
-------------------------------------------------------------------------------------------------------
Analisando as condições atuais do local, identifiquei que o risco de propagação de incêndio é {nivel}.
A combinação de temperatura em {temp} °C, umidade em {umidade}% e ventos de {vento} km/h indica que o fogo pode se deslocar principalmente em direção ao {direcao}.
Por precaução, evite áreas de vegetação mais densa e mantenha-se atento a qualquer mudança no ambiente.
Se desejar, posso continuar acompanhando a situação e te avisar caso haja alteração significativa.
    """

    return {
        "risco": risco,
        "nivel": nivel,
        "direcao": direcao,
        "mensagem": resposta.strip()
    }
