import matplotlib.pyplot as plt
import openpyxl
from openpyxl.drawing.image import Image

# Gerar gráfico de pizza


def gerar_grafico_pizza():
    # Exemplo de dados para gráfico
    categorias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    volumes = [150, 180, 120, 200, 160]

    # Gráfico de pizza
    plt.pie(volumes, labels=categorias, autopct='%1.1f%%', startangle=90)
    plt.title('Distribuição de Chamadas por Dia')

    # Salvar o gráfico como imagem
    plt.savefig('grafico_pizza.png')
    plt.close()

# Gerar gráfico de pizza e inserir no Excel


def criar_excel_com_grafico_pizza():
    gerar_grafico_pizza()

    # Criando uma planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resultados"

    # Adicionando dados na planilha
    categorias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    volumes = [150, 180, 120, 200, 160]

    ws.append(["Dia da Semana", "Volume de Chamadas"])
    for dia, volume in zip(categorias, volumes):
        ws.append([dia, volume])

    # Inserir o gráfico no Excel
    img = Image('grafico_pizza.png')
    ws.add_image(img, 'E5')  # A imagem será inserida na célula E5

    # Salvar o arquivo Excel
    wb.save("resultado_com_grafico_pizza.xlsx")


# Executar a função para gráfico de pizza
criar_excel_com_grafico_pizza()
print("Arquivo Excel com gráfico de pizza gerado com sucesso!")
