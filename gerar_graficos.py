import plotly.graph_objects as go
import openpyxl
from openpyxl.drawing.image import Image

# Exemplo de dados para gráfico baseado nos dias de um mês
dias_mes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
volumes = [120, 150, 130, 170, 200, 180, 160, 190, 210, 220, 240, 250, 220, 210,
           230, 190, 170, 180, 200, 220, 240, 250, 270, 280, 300, 290, 310, 320, 340, 350]

# Criar gráfico de barras interativo com Plotly


def gerar_grafico_barras_interativo():
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dias_mes,
        y=volumes,
        marker_color='skyblue',
        name='Volume de Chamadas'
    ))

    fig.update_layout(
        title='Volume de Chamadas por Dia no Mês',
        xaxis_title='Dia do Mês',
        yaxis_title='Volume de Chamadas',
        template='plotly_dark'
    )

    # Salvar o gráfico como imagem interativa
    fig.write_image('grafico_barras_interativo.png')

# Criar gráfico de pizza interativo com Plotly


def gerar_grafico_pizza_interativo():
    fig = go.Figure(data=[go.Pie(
        labels=dias_mes,
        values=volumes,
        hoverinfo="label+percent",
        textinfo="value+percent",
        hole=0.3
    )])

    fig.update_layout(
        title='Distribuição de Chamadas por Dia no Mês',
        template='plotly_dark'
    )

    # Salvar o gráfico como imagem interativa
    fig.write_image('grafico_pizza_interativo.png')

# Criar o arquivo Excel com gráfico de barras


def criar_excel_com_grafico_barras():
    gerar_grafico_barras_interativo()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resultados"

    # Adicionando dados na planilha
    ws.append(["Dia do Mês", "Volume de Chamadas"])
    for dia, volume in zip(dias_mes, volumes):
        ws.append([dia, volume])

    # Inserir o gráfico no Excel
    img = Image('grafico_barras_interativo.png')
    ws.add_image(img, 'E5')  # A imagem será inserida na célula E5

    # Salvar o arquivo Excel
    wb.save("resultado_com_grafico_barras_interativo.xlsx")

# Criar o arquivo Excel com gráfico de pizza


def criar_excel_com_grafico_pizza():
    gerar_grafico_pizza_interativo()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resultados"

    # Adicionando dados na planilha
    ws.append(["Dia do Mês", "Volume de Chamadas"])
    for dia, volume in zip(dias_mes, volumes):
        ws.append([dia, volume])

    # Inserir o gráfico no Excel
    img = Image('grafico_pizza_interativo.png')
    ws.add_image(img, 'E5')  # A imagem será inserida na célula E5

    # Salvar o arquivo Excel
    wb.save("resultado_com_grafico_pizza_interativo.xlsx")


# Executar as funções para gerar os gráficos e salvar os arquivos Excel
criar_excel_com_grafico_barras()
criar_excel_com_grafico_pizza()

print("Arquivos Excel com gráficos interativos de barras e pizza gerados com sucesso!")
