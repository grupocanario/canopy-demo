import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import plotly.express as px
from plotly import graph_objs as go
from urllib.request import urlopen
import json

# Loading dataframes
from data import df_national_covid


# GRAPHS ----------------------

# 1. Colombia cloropleth map: Number of contracts per department

with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json') as response:
    departments = json.load(response)

fig_map_2 = px.choropleth_mapbox(df_national_covid,
                           geojson=departments,
                           locations='Code',
                           color='Num. contratos',
                           featureidkey='properties.DPTO',
                           hover_name='Departamento',
                           color_continuous_scale="Mint",
                           range_color=(0, max(df_national_covid['Num. contratos'])),
                           mapbox_style="carto-positron",
                           zoom=4,
                           center = {"lat": 4.570868, "lon": -74.2973328},
                           opacity=0.5
                          )
fig_map_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                         html.Div(
                                            'Panorama General', 
                                            className='mx-auto title-visor'
                                         ),
                                    ],
                                    className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                ),
                            ],
                            className='text-left p-5'
                        ),
                        # Title
                        html.Div(
                            [
                                html.P(
                                    """
                                    Antes de comenzar a explorar todas las alertas que hemos creado, en 
                                    esta sección podrás ver un panorama general de cómo se han manejado 
                                    los contratos en referencia al COVID-19 dentro del territorio colombiano.
                                    Las siguientes gráficas visualizan el número de contrataciones que se han 
                                    realizado para atender a la emergencia por departamento, y un panorama general 
                                    de las alarmas construidas. 
                                    """
                                ),
                                html.P(
                                    """
                                    Para conocer el número de contratos en el mapa, pon tu cursor sobre 
                                    el departamento que quieres revisar. Y para las otras visualizaciones 
                                    de datos que hemos generado, podrás ver cómo las dividido los niveles 
                                    de alerta en tres categorías diferenciadas por color:
                                    """
                                ),
                            ],
                            className='text-left pl-5 pr-5 text-center'
                        ),
                    ],
                    className='px-5 mx-5',
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    'Visualización de datos', 
                                    className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                ),
                                dcc.Graph(figure=fig_map_2, className='div-for-graph-border')
                            ],
                            className='col div-for-graph-card'
                        ),
                        html.Div(
                            [
                                html.Div(
                                    'Visualización de datos', 
                                    className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                ),
                                dcc.Graph(figure=fig_map_2, className='div-for-graph-border')
                            ],
                            className='col div-for-graph-card'
                        ),
                    ],
                    className='row',
                ),
            ],
            className='mb-5',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    'Visualización de datos', 
                                    className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                ),
                                html.P(
                                    """
                                    Para consultar los datos de los 10 contratistas que concentran
                                    la adjudicación de contratos por departamento, puede acceder a
                                    ellos en la siguiente tabla. Al aplicar el filtro de interés podrá
                                    consultar nombre del contratista, NIT o C.C, valor total del contrato
                                    y departamento correspondiente.
                                    """
                                )
                            ],
                            className='text-left p-5'
                        ),
                        # Title
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            'Visualización de datos', 
                                            className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                        ),
                                        dcc.Graph(figure=fig_map_2, className='div-for-graph-border')
                                    ],
                                    className='col div-for-graph-card'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            'Visualización de datos', 
                                            className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                        ),
                                        dcc.Graph(figure=fig_map_2, className='div-for-graph-border')
                                    ],
                                    className='col div-for-graph-card'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            'Visualización de datos', 
                                            className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                        ),
                                        dcc.Graph(figure=fig_map_2, className='div-for-graph-border')
                                    ],
                                    className='col div-for-graph-card'
                                )
                            ],
                            className='row pl-5 pr-5'
                        ),
                    ],
                ),
            ],
            className='mb-5',
        ),
    ]
)