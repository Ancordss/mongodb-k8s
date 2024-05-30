from flask import Flask, jsonify, render_template, request
import requests
import plotly.express as px
import pandas as pd
import os

app = Flask(__name__)

# Configura la URL del servicio de datos
DATA_SERVICE_URL = "http://localhost:5000"
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", DATA_SERVICE_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart/estado_asuntos')
def chart_estado_asuntos():
    response = requests.get(f"{DATA_SERVICE_URL}/grafica/estado_asuntos")
    data = response.json()

    df = pd.DataFrame(data)
    fig = px.pie(df, names='_id', values='count', title='Distribución de Estados de Asuntos')
    graph_html = fig.to_html(full_html=False)
    
    return render_template('chart.html', graph_html=graph_html)


@app.route('/chart/abogados_por_gabinete')
def chart_abogados_por_gabinete():
    response = requests.get(f"{DATA_SERVICE_URL}/grafica/abogados_por_gabinete")
    data = response.json()

    df = pd.DataFrame(data)
    fig = px.bar(df, x='_id', y='count', title='Número de Abogados por Gabinete')
    graph_html = fig.to_html(full_html=False)
    
    return render_template('chart.html', graph_html=graph_html)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
