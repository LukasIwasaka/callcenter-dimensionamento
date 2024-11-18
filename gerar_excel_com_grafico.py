import matplotlib.pyplot as plt
import openpyxl
from openpyxl.drawing.image import Image

# Exemplo de dados para gráfico baseado nos dias de um mês
dias_mes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
volumes = [120, 150, 130, 170, 200, 180, 160, 190, 210, 220, 240, 250, 220, 210,
           230, 190, 170, 180, 200, 220, 240, 250, 270, 280, 300, 290, 310, 320, 340, 350]

# Gerar gráfico de barras


def gerar_grafico_barras():
    plt.bar(dias_mes, volumes)
    plt.xlabel('Dia do Mês')
    plt.ylabel('Volume de Chamadas')
    plt.title('Volume de Chamadas por Dia no Mês')
    plt.xticks(rotation=45)  # Rotaciona os rótulos para melhor visualização
    plt.tight_layout()

    # Salvar o gráfico como imagem
    plt.savefig('grafico_barras_dia_mes.png')
    plt.close()

# Gerar gráfico de pizza


def gerar_grafico_pizza():
    plt.pie(volumes, labels=dias_mes, autopct='%1.1f%%', startangle=90)
    plt.title('Distribuição de Chamadas por Dia no Mês')

    # Salvar o gráfico como imagem
    plt.savefig('grafico_pizza_dia_mes.png')
    plt.close()

# Criar o arquivo Excel com gráfico de barras


def criar_excel_com_grafico_barras():
    gerar_grafico_barras()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resultados"

    # Adicionando dados na planilha
    ws.append(["Dia do Mês", "Volume de Chamadas"])
    for dia, volume in zip(dias_mes, volumes):
        ws.append([dia, volume])

    # Inserir o gráfico no Excel
    img = Image('grafico_barras_dia_mes.png')
    ws.add_image(img, 'E5')  # A imagem será inserida na célula E5

    # Salvar o arquivo Excel
    wb.save("resultado_com_grafico_barras_dia_mes.xlsx")

# Criar o arquivo Excel com gráfico de pizza


def criar_excel_com_grafico_pizza():
    gerar_grafico_pizza()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resultados"

    # Adicionando dados na planilha
    ws.append(["Dia do Mês", "Volume de Chamadas"])
    for dia, volume in zip(dias_mes, volumes):
        ws.append([dia, volume])

    # Inserir o gráfico no Excel
    img = Image('grafico_pizza_dia_mes.png')
    ws.add_image(img, 'E5')  # A imagem será inserida na célula E5

    # Salvar o arquivo Excel
    wb.save("resultado_com_grafico_pizza_dia_mes.xlsx")


# Executar as funções para gerar os gráficos e salvar os arquivos Excel
criar_excel_com_grafico_barras()
criar_excel_com_grafico_pizza()

print("Arquivos Excel com gráficos de barras e pizza gerados com sucesso!")
