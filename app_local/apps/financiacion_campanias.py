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



import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import plotly.express as px
from plotly import graph_objs as go
from urllib.request import urlopen
import json

from data import df_national_covid

from app import app
from data import df_proov, df_proov_cum

# Table parameters ------------
PAGE_SIZE = 10
PAGE_SIZE_CONTRATISTAS = 3

# Dash components ---------

# Table
steps_header = [html.Thead(
    html.Tr(
            html.Div(
            'Pasos para filtrar', 
            className='font-weight-bold text-steps font-medium py-2',
        ),
    ),
)]

row1 = html.Tr([html.P("1. Comienza la búsqueda filtrando por el departamento tu interés.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row2 = html.Tr([html.P("2. En la tabla podrás ver el costo de los contratos adjudicados, y los datos del respectivo financiador.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row3 = html.Tr([html.P("3. Para más información puedes ir al link de la SECOP ubicado al final de la tabla.", className='m-3 lead font-weight-normal text-dark font-home-m')])

steps_body = [html.Tbody([row1, row2, row3])]


steps_table = html.Table(steps_header + steps_body)

# Filters table
filter_depto_fin = dcc.Dropdown(
    options=[{'label': i, 'value': i} for i in df_proov.Departamento.drop_duplicates()],
    value=None,
    id='filter-depto-fin',
)  

# GRAPHS ----------------------

# 1. Colombia cloropleth map: Number of contracts per department

with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json') as response:
    departments = json.load(response)

fig_map_2 = px.choropleth_mapbox(df_proov_cum,
                           geojson=departments,
                           locations='Code',
                           color='Pct proveedores',
                           featureidkey='properties.DPTO',
                           hover_name='Departamento',
                           color_continuous_scale="Mint",
                        #    color_continuous_scale=["#FFF1A8", "#FFD608"],
                           range_color=(min(df_proov_cum['Pct proveedores']), max(df_proov_cum['Pct proveedores'])),
                           mapbox_style="carto-positron",
                           zoom=4,
                           center = {"lat": 4.570868, "lon": -74.2973328},
                           opacity=0.5
                          )
fig_map_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# 2. Bar Plot

trace_1 = go.Bar(x=df_proov_cum['Pct proveedores'], y=df_proov_cum['Departamento'], orientation='h')

layout = go.Layout(hovermode = 'closest')
fig = go.Figure(data = [trace_1], layout = layout)#
fig.update_layout(
    font=dict(
        color="#252525",
        family="Roboto"
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="% concentracion 10 primeros contratistas",
    yaxis=dict(dtick = 1),
    margin={"r":0,"t":0,"l":0,"b":0}
)
fig.update_traces(marker_color='#FFD608')

# Section layout --------------------

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
                                            className='py-5 back-financiacion'
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.Div(
                                                                            "Alerta: Financiación de campañas",
                                                                            className = 'mx-auto title-visor',
                                                                            style={'display': 'inline-block'}
                                                                        ),
                                                                    ],
                                                                    className='display-4 font-weight-bold text-home-title font-medium pb-4',
                                                                ),
                                                                html.Div(
                                                                    [
                                                                        html.P(
                                                                            """
                                                                            En esta sección podrás acceder a una base de datos donde se muestra quiénes de los contratistas a los que se le adjudicaron contratos financiaron campañas políticas.
                                                                            Adicionalmente podrás observar los partidos políticos y el candidato que fueron financiados por estos contratistas. 
                                                                            """, 
                                                                            className='lead font-weight-normal text-dark font-home-m'
                                                                        ),
                                                                    ],
                                                                    className='mb-5',
                                                                ),
                                                                
                                                            ], 
                                                            className='justify-content-center mx-5 mt-5 pt-5 pb-2 paragraph-alerta',
                                                        ),
                                                    ],
                                                    className='col',
                                                ),
                                                html.Div(
                                                    [
                                                        steps_table
                                                    ], 
                                                    className='col-4 justify-content-center mx-5 px-5 pt-5 pb-2',
                                                ),
                                            ],
                                            className='row pb-5 div-for-alerta-financiacion',
                                        ),

                                        html.Div(
                                            [
                                                html.A(
                                                    'Ver Mas', 
                                                    className='btn btn-outline-secondary p-3 text-dark font-home-m btn-ver-alerta', 
                                                    href="#graficas-fin",
                                                ),
                                            ],
                                            className='row mx-auto justify-content-center mt-5',
                                        ),
                                        
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            'Mapa', 
                                                            className='row mb-2 pb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                                                        ),
                                                        dcc.Graph(figure=fig_map_2, className='div-for-graph-border')
                                                    ],
                                                    className='col div-for-graph-card div-for-graph-individual'
                                                ),
                                            ],
                                            className='row',
                                        ),
                                    ],
                                ),
                            ],
                            className='row pb-5',
                        ),
                    ],
                    className='mx-auto mb-5 mt-1',
                ),
            ],
        ),
        html.Div (
            [
                html.Div(
                    [
                        dbc.Card(
                            [
                                html.Div (
                                    [
                                        html.Div(
                                            "Concentracion de contratistas",
                                            className= 'col align-items-center text-header-table',
                                            style={'display': 'flex'},
                                        ),
                                        html.Div(
                                            [
                                                html.Div('Filtrar por departamento', className='text-header-table pb-2'),
                                                filter_depto_fin
                                            ],
                                            className='col pr-5'
                                        ),
                                    ],
                                    className='row p-5'
                                ),                                
                                html.Div (
                                    [
                                        html.Div(
                                            id='table-financiacion',
                                            className='table my-0 div-for-table-alertas'
                                        ),
                                    ],
                                    className='row mx-0',
                                ),
                                html.Div (
                                    [
                                        html.Div(
                                            id='count_entries-fin',
                                            className='col my-auto',
                                        ),
                                        html.Div(
                                            className='col my-auto buttons-footer-table',
                                            children=[
                                                    dbc.Button("Anterior", id='previous-page-fin', n_clicks=0, className='buttons-footer'), 
                                                    dbc.Button("Siguiente", id='next-page-fin', n_clicks=0, className='buttons-footer'),
                                            ],
                                        ),
                                    ],
                                    className='row mai-datatable-footer'
                                ),
                            ],
                            className='border-0',
                        ),
                    ],
                    className='container',
                ),
            ],
            className='main-content-table',
        ),
    ]
)

MIN_VAL_CAMPANIAS = 0
MAX_VAL_CAMPANIAS = 10
NUM_ENTRIES_CAMPANIAS = 10

def reload_table_counters():
    global MIN_VAL_CAMPANIAS
    global MAX_VAL_CAMPANIAS
    global NUM_ENTRIES_CAMPANIAS
    MIN_VAL_CAMPANIAS = 0
    MAX_VAL_CAMPANIAS = 10
    NUM_ENTRIES_CAMPANIAS = 10
    return MIN_VAL_CAMPANIAS, MAX_VAL_CAMPANIAS, NUM_ENTRIES_CAMPANIAS


# create callback for modifying page layout
@app.callback(
    [Output("table-financiacion", "children"),
    Output("count_entries-fin", "children"),
    Output("previous-page-fin", "disabled"),
    Output("next-page-fin", "disabled")], 
    [Input('previous-page-fin', 'n_clicks'),
    Input('next-page-fin', 'n_clicks'),
    Input('filter-depto-fin', 'value')])
def update_table(btn_prev, btn_next, depto_filter):

    global MIN_VAL_CAMPANIAS
    global MAX_VAL_CAMPANIAS
    global NUM_ENTRIES_CAMPANIAS
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'filter-depto-fin' in changed_id and depto_filter != None:
        MIN_VAL_CAMPANIAS = 0
        MAX_VAL_CAMPANIAS = 10
        df_subset = df_proov[df_proov['Departamento']==depto_filter]


    if depto_filter != None:
        df_subset = df_proov[df_proov['Departamento']==depto_filter]
    else:
        df_subset = df_proov.copy()

    LEN_DF_COMPLETE_ITEMS = len(df_subset)

    # Sorting table
    df_subset = df_subset.sort_values(by='Pct acumulado de contratos')

    if 'previous-page-fin' in changed_id:
        MIN_VAL_CAMPANIAS = max(0, MIN_VAL_CAMPANIAS-NUM_ENTRIES_CAMPANIAS-1)
        MAX_VAL_CAMPANIAS = min(LEN_DF_COMPLETE_ITEMS, MAX_VAL_CAMPANIAS-NUM_ENTRIES_CAMPANIAS-1)
    elif 'next-page-fin' in changed_id:
        MIN_VAL_CAMPANIAS = max(0, MIN_VAL_CAMPANIAS+NUM_ENTRIES_CAMPANIAS+1)
        MAX_VAL_CAMPANIAS = min(LEN_DF_COMPLETE_ITEMS, MAX_VAL_CAMPANIAS+NUM_ENTRIES_CAMPANIAS+1)

    if MIN_VAL_CAMPANIAS < 1:
        disabled_prev = True
    else:
        disabled_prev = False

    if MAX_VAL_CAMPANIAS >= LEN_DF_COMPLETE_ITEMS:
        disabled_next = True
    else:
        disabled_next = False

    df_subset = df_subset.iloc[MIN_VAL_CAMPANIAS:MAX_VAL_CAMPANIAS,:]

    table_final = html.Table(
        # Header
        [html.Thead([html.Th(col) for col in df_subset.columns]) ] +
        # Body - Here we stablish the link
        [html.Tr(
                # List comprehension
                [
                    html.Td(df_subset.iloc[i][col]) if col != 'SECOP URL' 
                    # Link to SECOP URL
                    else html.Td(
                        html.A(html.I(className="fas fa-external-link-alt", style={'color': '#238ae5'}), href=df_subset.iloc[i][col],), 
                        className='text-center',
                        ) 
                    for col in df_subset.columns
                ]
            )
        for i in range(min(len(df_subset), 20))],
        # className="table border-collapse",
        # id='table-financiacion',
        style={"overflowY": "scroll", 'width': '100%'}
    )

    text_entries = 'Mostrando {} a {} de {} resultados'.format(MIN_VAL_CAMPANIAS+1, min(LEN_DF_COMPLETE_ITEMS, MAX_VAL_CAMPANIAS+1), LEN_DF_COMPLETE_ITEMS)
    
    return table_final, text_entries, disabled_prev, disabled_next