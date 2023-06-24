from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from io import StringIO
import sys

# URL del archivo Python en GitHub
url = "https://raw.githubusercontent.com/dereckamesquita/bcrp-scrapper/main/bcrp_scrapper.py"

try:
    # Descargar el archivo desde GitHub
    response = requests.get(url)
    response.raise_for_status()

    # Crear un objeto StringIO para leer el contenido del archivo descargado
    file_content = StringIO(response.text)

    # Importar el archivo descargado como un módulo
    module = type(sys)("bcrp_scrapper")
    exec(file_content.read(), module.__dict__)

    # Importar las funciones o variables necesarias del módulo
    from module import *

    # Ahora puedes usar las funciones o variables importadas
    # ...
    # ...
except requests.exceptions.RequestException as e:
    print(f"Error al descargar el archivo: {e}")

from bcrp_scrapper import *

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
data = {'Nombre': ['Juan', 'María', 'Carlos'],
        'Edad': [25, 30, 35],
        'Ciudad': ['Lima', 'Bogotá', 'Santiago']}

df = pd.DataFrame(data)

# Mostrar el DataFrame en Streamlit
df = bcrpscrapper(bcrp)
st.dataframe(df)

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
