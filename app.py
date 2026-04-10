from flask import Flask, render_template, request

app = Flask(__name__)

# ── Conversões ──────────────────────────────────────────────

def converter_temperatura(valor, de, para):
    # Converte tudo para Celsius primeiro
    if de == "celsius":
        celsius = valor
    elif de == "fahrenheit":
        celsius = (valor - 32) * 5 / 9
    elif de == "kelvin":
        celsius = valor - 273.15

    # Celsius para destino
    if para == "celsius":
        return celsius
    elif para == "fahrenheit":
        return celsius * 9 / 5 + 32
    elif para == "kelvin":
        return celsius + 273.15


def converter_peso(valor, de, para):
    # Tudo para gramas
    para_gramas = {
        "grama": 1,
        "kilograma": 1000,
        "libra": 453.592,
        "onca": 28.3495,
        "tonelada": 1_000_000,
    }
    em_gramas = valor * para_gramas[de]
    return em_gramas / para_gramas[para]


def converter_moeda(valor, de, para):
    # Taxas fixas em relação ao BRL
    taxas = {
        "BRL": 1,
        "USD": 5.05,
        "EUR": 5.50,
        "GBP": 6.40,
        "ARS": 0.006,
        "JPY": 0.034,
    }
    em_brl = valor * taxas[de]
    return em_brl / taxas[para]


# ── Rotas ────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/converter", methods=["POST"])
def converter():
    tipo = request.form.get("tipo")
    resultado = None
    erro = None

    try:
        valor = float(request.form.get("valor", 0))
        de = request.form.get("de")
        para = request.form.get("para")

        if de == para:
            resultado = valor
        elif tipo == "temperatura":
            resultado = converter_temperatura(valor, de, para)
        elif tipo == "peso":
            resultado = converter_peso(valor, de, para)
        elif tipo == "moeda":
            resultado = converter_moeda(valor, de, para)

        resultado = round(resultado, 4)

    except Exception as e:
        erro = "Valor inválido. Digite um número correto."

    return render_template("index.html",
                           resultado=resultado,
                           erro=erro,
                           tipo_ativo=tipo,
                           valor=request.form.get("valor"),
                           de=de,
                           para=para)


if __name__ == "__main__":
    app.run(debug=True)
