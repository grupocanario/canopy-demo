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



from app import app

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np


from data import df_items


# Dash components ---------

# Table
steps_header_items = [html.Thead(
    html.Tr(
            html.Div(
            'Pasos para filtrar', 
            className='font-weight-bold text-steps font-medium py-2',
        ),
    ),
)]

row1 = html.Tr([html.P("1. Comienza la búsqueda filtrando por el departamento tu interés.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row2 = html.Tr([html.P("2. En la primera columna de cada contrato podrás ver marcado con amarillo los contratos que presentan un sobrecosto, y en gris aquellos que no tienen la alerta.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row3 = html.Tr([html.P("3. Podrás ver los datos mas importantes de cada contrato, junto con información del item que se contrató.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row4 = html.Tr([html.P("4. Para más información puedes ir al link de la SECOP ubicado en la última columna de la tabla.", className='m-3 lead font-weight-normal text-dark font-home-m')])

steps_body_items = [html.Tbody([row1, row2, row3, row4])]


steps_table_items = html.Table(steps_header_items + steps_body_items)

# Filters table
filter_depto_items = dcc.Dropdown(
    options=[{'label': i, 'value': i} for i in df_items.Departamento.drop_duplicates()],
    value=None,
    id='filter-depto-items',
)  




# Section layout --------------------

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            className='py-5 back-sobrecosto'
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
                                                            "Alerta: Sobrecosto en Items",
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
                                                            En esta sección se muestra cuáles contratos de SECOP II tienen o no un sobrecosto en los productos adquiridos. En la tabla podrás observar todos los datos de la contratación, y  visualizar el precio máximo que tiene el ítem dentro de los Acuerdos Marco (precio máximo de mercado) comparado con el costo que tuvo dentro del contrato. 
                                                            """, 
                                                            className='lead font-weight-normal text-dark font-home-m'
                                                        ),
                                                        dbc.Alert(
                                                            """
                                                            Advertencia: Esta alarma se encuentra actualizada hasta el 15 de Junio de 2020, debido a que 
                                                            Colombia Compra Eficiente implementó un sistema de CAPTCHA en SECOP II a partir de Agosto de 2020. 
                                                            """,
                                                             color="warning", style={'font-size':'15px'}, className='mt-5'
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
                                        steps_table_items
                                    ], 
                                    className='col-4 justify-content-center mx-5 px-5 pt-5 pb-2',
                                ),
                            ],
                            className='row pb-5 div-for-alerta-sobrecosto',
                        ),
                        html.Div(
                            [
                                html.A(
                                    'VER ALERTA', 
                                    className='btn btn-outline-secondary p-3 text-dark font-home-m btn-ver-alerta', 
                                    href="#tabla-container",
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
                                        dcc.Graph(className='div-for-graph-border div-for-graph-individual')
                                    ],
                                    className='col div-for-graph-card'
                                ),
                            ],
                            className='row',
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
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.Span(className='dot mr-3'),
                                                                "Tiene alerta de sobrecosto",
                                                                html.Br(), 
                                                                html.Span(className='dot-gray mr-3'), 
                                                                "No tiene alerta de sobrecosto"
                                                            ]
                                                        ),
                                                    ],
                                                    className = 'row'
                                                ),
                                            ],
                                            className= 'col align-items-center text-header-table',
                                            style={'display': 'flex'},
                                        ),
                                        html.Div(
                                            [
                                                html.Div('Filtrar por departamento', className='text-header-table pb-2'),
                                                filter_depto_items
                                            ],
                                            className='col pr-5'
                                        ),
                                    ],
                                    className='row p-5'
                                ),                                
                                html.Div (
                                    [
                                        html.Div(
                                            id='table-items',
                                            className='table my-0 div-for-table-alertas'
                                        ),
                                    ],
                                    className='row mx-0',
                                ),
                                html.Div (
                                    [
                                        html.Div(
                                            id='count_entries-items',
                                            className='col my-auto',
                                        ),
                                        html.Div(
                                            className='col my-auto buttons-footer-table',
                                            children=[
                                                    dbc.Button("Anterior", id='previous-page-items', n_clicks=0, className='buttons-footer'), 
                                                    dbc.Button("Siguiente", id='next-page-items', n_clicks=0, className='buttons-footer'),
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
            id="tabla-container",
        ),
    ]
)

MIN_VAL_SOBRECOSTO = 0
MAX_VAL_SOBRECOSTO = 10
NUM_ENTRIES_SOBRECOSTO = 10

def reload_table_counters():
    global MIN_VAL_SOBRECOSTO
    global MAX_VAL_SOBRECOSTO
    global NUM_ENTRIES_SOBRECOSTO
    MIN_VAL_SOBRECOSTO = 0
    MAX_VAL_SOBRECOSTO = 10
    NUM_ENTRIES_SOBRECOSTO = 10
    return MIN_VAL_SOBRECOSTO, MAX_VAL_SOBRECOSTO, NUM_ENTRIES_SOBRECOSTO


# create callback for modifying page layout
@app.callback(
    [Output("table-items", "children"),
    Output("count_entries-items", "children"),
    Output("previous-page-items", "disabled"),
    Output("next-page-items", "disabled")
    ], 
    [Input('previous-page-items', 'n_clicks'),
    Input('next-page-items', 'n_clicks'),
    Input('filter-depto-items', 'value')])
def update_table(btn_prev, btn_next, depto_filter):

    global MIN_VAL_SOBRECOSTO
    global MAX_VAL_SOBRECOSTO
    global NUM_ENTRIES_SOBRECOSTO
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'filter-depto' in changed_id and depto_filter != None:
        MIN_VAL_SOBRECOSTO = 0
        MAX_VAL_SOBRECOSTO = 10
        df_subset = df_items[df_items['Departamento']==depto_filter]


    if depto_filter != None:
        df_subset = df_items[df_items['Departamento']==depto_filter]
    else:
        df_subset = df_items.copy()

    LEN_DF_COMPLETE_ITEMS = len(df_subset)


    if 'previous-page-items' in changed_id:
        MIN_VAL_SOBRECOSTO = max(0, MIN_VAL_SOBRECOSTO-NUM_ENTRIES_SOBRECOSTO-1)
        MAX_VAL_SOBRECOSTO = max(min(LEN_DF_COMPLETE_ITEMS, MAX_VAL_SOBRECOSTO-NUM_ENTRIES_SOBRECOSTO-1), NUM_ENTRIES_SOBRECOSTO)
    elif 'next-page-items' in changed_id:
        MIN_VAL_SOBRECOSTO = max(0, MIN_VAL_SOBRECOSTO+NUM_ENTRIES_SOBRECOSTO+1)
        MAX_VAL_SOBRECOSTO = min(LEN_DF_COMPLETE_ITEMS, MAX_VAL_SOBRECOSTO+NUM_ENTRIES_SOBRECOSTO+1)

    if MIN_VAL_SOBRECOSTO < 1:
        disabled_prev = True
    else:
        disabled_prev = False

    if MAX_VAL_SOBRECOSTO == LEN_DF_COMPLETE_ITEMS:
        disabled_next = True
    else:
        disabled_next = False

    df_subset = df_subset.iloc[MIN_VAL_SOBRECOSTO:MAX_VAL_SOBRECOSTO,:]

    table_final = [html.Table(
        # Header
        [html.Thead([html.Th(col) for col in df_subset.columns]) ] +
        # Body - Here we stablish the link
        [html.Tr(
                # List comprehension
                [
                    html.Td(
                        df_subset.iloc[i][col]) 
                        if ((col != 'SECOP URL')&(col != 'Alerta de sobrecosto'))
                        # Link to SECOP URL
                        else html.Td(
                            html.Span(className='dot'), 
                            className='text-center',
                            ) 
                        if ((col == 'Alerta de sobrecosto')&(df_subset.iloc[i][col]=='Si'))
                        else html.Td(
                            html.Span(className='dot-gray'), 
                            className='text-center',
                            ) 
                        if (((col == 'Alerta de sobrecosto')&(df_subset.iloc[i][col]!='Si')))
                        else html.Td(
                            html.A(html.I(className="fas fa-external-link-alt", style={'color': '#238ae5'}), href=df_subset.iloc[i][col],), 
                            className='text-center',
                        )
                    for col in df_subset.columns
                ]
            )
        for i in range(min(len(df_subset), 20))],
        # # className="table border-collapse",
        # id='table-items',
        style={"overflowY": "scroll"}
    )]

    text_entries = 'Mostrando {} a {} de {} resultados'.format(MIN_VAL_SOBRECOSTO+1, min(LEN_DF_COMPLETE_ITEMS, MAX_VAL_SOBRECOSTO+1), LEN_DF_COMPLETE_ITEMS)
    
    return table_final, text_entries, disabled_prev, disabled_next