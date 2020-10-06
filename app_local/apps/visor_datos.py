# --------------------
# Copyright (c) 2020 Grupo Canario

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import plotly.express as px
from plotly import graph_objs as go
from urllib.request import urlopen
import json

# Loading dataframes
from data import df_national_covid, df_summary


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

# 1. Colombia cloropleth map: Number of contracts per department
fig_summary = px.bar(df_summary, x="Número de alertas", y="Alerta", orientation='h',
             height=500)
fig_summary.update_layout(
    font=dict(
        color="#252525",
        family="Roboto"
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Numero de contratos con alertas",
    yaxis_title='',
    margin={"r":0,"t":0,"l":0,"b":0}
)


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
                                    Antes de comenzar a explorar todas las alertas que hemos creado, en esta sección podrás ver un panorama general de cómo se han manejado los contratos en referencia al COVID-19 dentro del territorio colombiano. Las siguientes gráficas visualizan el número de contrataciones que se han realizado para atender a la emergencia por departamento, y un panorama general de las alarmas construidas.
                                    """
                                ),
                                html.P(
                                    """
                                    Explora las gráficas que explican el panorama de contratación en el pais y un overview del número de alertas que hemos identificado. 

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
                                    'Contratación nacional para COVID-19', 
                                    className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            """
                                            Número total de contratos emitidos por cada departamento para atender la emergencia.
                                            """
                                        ), 
                                    ],
                                    className='text-left pl-5 pr-5 text-center'
                                ), 
                                dcc.Graph(figure=fig_map_2, className='div-for-graph-border')
                            ],
                            className='col div-for-graph-card'
                        ),
                            # html.Div(
                            #     [
                            #         html.Div(
                            #             'Alertas tempranas de contratación', 
                            #             className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                            #         ),
                            #         html.Div(
                            #             [
                            #                 html.P(
                            #                     """
                            #                     Número de contratos detectados de COVID-19 con alertas para cada una de las categorías. 
                            #                     """
                            #                 ),
                            #             ],
                            #             className='text-left pl-5 pr-5 text-center'
                            #         ), 
                            #         dcc.Graph(figure=fig_summary, className='div-for-graph-border')
                            #     ],
                            #     className='col div-for-graph-card'
                            # ),
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
                                    'Resumen de Alertas Tempranas', 
                                    className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            """
                                            Para el proyecto Canopy construimos 4 alertas tempranas, cada una reflejando posibles riesgos en el proceso de contratación en la emergencia del COVID-19. Para más información sobre una alerta específica, dirígete a la pestaña Alertas Tempranas y escoge la alerta de tu interés.
                                            """
                                        ),
                                    ],
                                    className='text-center pr-5'
                                ),
                            ],
                            className='text-left p-5'
                        ),
                        # Title
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            'Alerta Sobrecosto', 
                                            className='row mb-2 display-4 font-weight-bold text-h2 mx-auto font-medium',
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            'Alerta Transparencia', 
                                            className='row mb-2 display-4 font-weight-bold text-h2 mx-auto  font-medium',
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            'Concentración de contratistas', 
                                            className='row mb-2 display-4 font-weight-bold text-h2 mx-auto font-medium',
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                 html.Div(
                                    [
                                        html.Div(
                                            'Financiación de campañas', 
                                            className='row mb-2 display-4 font-weight-bold text-h2 mx-auto font-medium',
                                        ),
                                    ],
                                    className='col pl-5'
                                )
                            ],
                            className='row pl-5 pr-5 py-3'
                        ),
                        # Texto
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    """
                                                    Esta alerta se concentra en contratos de compraventa de items destinados para la mitigación de la pandemia. Comparamos los precios por item reportados en SECOP vs. los precios máximos en los Acuerdos Marco de Colombia Compra Eficiente para evidenciar posibles sobrecostos. 
                                                    """
                                                ),
                                            ],
                                            className='text-left pr-5'
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    """
                                                    Esta alerta comprueba si NO fueron reportados en SECOP II dos partes importantes del proceso de contratación: los competidores y la etapa de planeación. 
                                                    """
                                                ),
                                            ],
                                            className='text-left pr-5'
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    """
                                                    En esta pestaña se muestra un indicador que refleja la concentración de la adjudicación de contratos por departamento en los 10 primeros contratistas. A mayor concentración en un departamento, mayor riesgo de concentracion de adjudicación de contratos. 
                                                    """
                                                ),
                                            ],
                                            className='text-left pr-5 '
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                 html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    """
                                                    Esta sección muestra quiénes de los contratistas a los que se le adjudicaron contratos financiaron campañas políticas. Los financiadores de campañas políticas se toman de la herramienta Monitor Ciudadano de Transparencia por Colombia. 
                                                    """
                                                ),
                                            ],
                                            className='text-left pr-5 '
                                        ),
                                    ],
                                    className='col pl-5'
                                )
                            ],
                            className='row pl-5 pr-5 pb-5'
                        ),
                        # Botones
                        html.Div(
                            [
                                html.Div(
                                    [
                                         html.A(
                                            'Ir a Sobrecosto', 
                                            className='btn btn-outline-secondary p-3 text-dark font-home-m btn-ver-alerta', 
                                            href="/alerta-sobrecosto",
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                html.Div(
                                    [
                                        html.A(
                                            'Ir a Transparencia', 
                                            className='btn btn-outline-secondary p-3 text-dark font-home-m btn-ver-alerta', 
                                            href="/alerta-transparencia",
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                html.Div(
                                    [
                                        html.A(
                                            'Ir a Concentración', 
                                            className='btn btn-outline-secondary p-3 text-dark font-home-m btn-ver-alerta', 
                                            href="/concentracion-contratistas",
                                        ),
                                    ],
                                    className='col pl-5'
                                ),
                                 html.Div(
                                    [
                                        html.A(
                                            'Ir a Financiación', 
                                            className='btn btn-outline-secondary p-3 text-dark font-home-m btn-ver-alerta', 
                                            href="/financiacion-campanias",
                                        ),
                                    ],
                                    className='col pl-5'
                                )
                            ],
                            className='row pl-5 pr-5 pb-5'
                        ),
                    ],
                    
                ),
            ],
            className='py-5',
            style={'background-color': '#f3f3f3'}
        ),
    ]
)