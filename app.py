from flask import Flask, jsonify, render_template
import random
import matplotlib.pyplot as plt
import io
import base64
# Verifique a importação
from call_volume_prediction import genetic_algorithm, calcular_volume_chamadas

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prever_volume')
def prever_volume():
    # Exemplo de valor real de volume de chamadas
    actual_call_volume = 100
    best_solution = genetic_algorithm(actual_call_volume)

    # Calculando o volume de chamadas
    predicted_volume = calcular_volume_chamadas(
        10, 300, 26, best_solution[4], best_solution[4], best_solution[3]
    )

    # Arredondando a previsão final
    rounded_predicted_volume = round(predicted_volume)

    return jsonify({
        'melhor_solucao': best_solution,
        'previsao_volume': rounded_predicted_volume
    })


@app.route('/grafico')
def grafico():
    # Exemplo de gráfico simples com dados aleatórios
    x = [i for i in range(10)]
    y = [random.randint(1, 100) for _ in range(10)]

    # Gerando o gráfico
    plt.figure()
    plt.plot(x, y)
    plt.title('Gráfico de Previsão de Volume')
    plt.xlabel('Dias')
    plt.ylabel('Volume de Chamadas')

    # Salvando o gráfico em formato base64 para exibição no front-end
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return render_template('grafico.html', img_base64=img_base64)


if __name__ == '__main__':
    app.run(debug=True)
