import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import json

# from home import app
from app import app

# DATAFRAMES -----------------

# 1. Dataframe SECOP I & II items
df_raw_items = pd.read_csv("https://storage.googleapis.com/secop_data/secop_join_suministros_w_sobrecosto.csv")
df_items = df_raw_items.copy()
df_items = df_items.rename(columns={
    'nombre_entidad': 'Nombre de la entidad',
    'departamento': 'Departamento',
    'ciudad': 'Municipio',
    'id_contrato': 'ID contrato',
    'descripcion_del_proceso': 'Descripcion del contrato',
    'tipo_de_contrato': 'Tipo de contrato',
    'modalidad_de_contratacion': 'Modalidad de contratacion',
    'proveedor_adjudicado': 'Proveedor adjudicado',
    'url': 'SECOP URL',
    'valor_del_contrato': 'Valor del contrato',
    'item_code': 'Código del item',
    'item_description': 'Descripción del item',
    'item_quantity': 'Cantidad del item',
    'item_price': 'Precio por item',
    'precio_piso': 'Precio minimo',
    'precio_techo': 'Precio maximo',
    'alarma_sobrecosto': 'Alerta de sobrecosto'
})

df_items = df_items[['Alerta de sobrecosto', 'Descripción del item', 'Nombre de la entidad', 'Departamento', 'Municipio', 'Proveedor adjudicado', 'Valor del contrato', 'Código del item',
              'Cantidad del item', 'Precio por item', 'Precio minimo', 'Precio maximo',
             'Descripcion del contrato', 'ID contrato',
             'Tipo de contrato', 'Modalidad de contratacion',  'SECOP URL']]
df_items['Alerta de sobrecosto'] = np.where(df_items['Alerta de sobrecosto']==True, 'Si', 'No')
df_items['SECOP URL'] = '[Link](' + df_items['SECOP URL'] + ')'


entidades_items = df_items['Municipio'].unique()


# 2. Dataframe SECOP I & II transparency
df_raw_transparency = pd.read_csv("https://storage.googleapis.com/secop_data/secop_2_covid_singleitem.csv")
df_transparency = df_raw_transparency.copy()
df_transparency = df_transparency.rename(columns={
    'nombre_entidad': 'Nombre de la entidad',
    'departamento': 'Departamento',
    'ciudad': 'Municipio',
    'id_contrato': 'ID contrato',
    'descripcion_del_proceso': 'Descripcion del contrato',
    'tipo_de_contrato': 'Tipo de contrato',
    'modalidad_de_contratacion': 'Modalidad de contratacion',
    'proveedor_adjudicado': 'Proveedor adjudicado',
    'url': 'SECOP URL',
    'valor_del_contrato': 'Valor del contrato',
    'items_per_contract': 'Items por contrato'
})

df_transparency = df_transparency[['Nombre de la entidad', 'Departamento', 'Municipio', 'Proveedor adjudicado', 'Valor del contrato',
             'Descripcion del contrato', 'ID contrato',
             'Tipo de contrato', 'Modalidad de contratacion',  'SECOP URL']]

df_transparency['SECOP URL'] = '[Link](' + df_items['SECOP URL'] + ')'


# Table parameters ------------
PAGE_SIZE = 10
PAGE_SIZE_CONTRATISTAS = 3

# Dash components ---------

# Table

dropdown_entries = dcc.Dropdown(
    id="dropdown-entries",
    value=10,
    options=[
        {"label": "10", "value": 10},
        {"label": "15", "value": 15},
        {"label": "25", "value": 25},
    ],
)

steps_header = [html.Thead(
    html.Tr(
            html.Div(
            'Pasos para filtrar', 
            className='font-weight-bold text-steps font-medium py-2',
        ),
    ),
)]

row1 = html.Tr([html.P("1. And an even wittier subheading to boot.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row2 = html.Tr([html.P("2. And an even wittier subheading to boot.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row3 = html.Tr([html.P("3. And an even wittier subheading to boot.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row4 = html.Tr([html.P("4. And an even wittier subheading to boot.", className='m-3 lead font-weight-normal text-dark font-home-m')])

steps_body = [html.Tbody([row1, row2, row3, row4])]


steps_table = html.Table(steps_header + steps_body)



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
                                            [
                                                html.Div(
                                                    'Alerta: Transparencia activa', 
                                                    className='display-4 font-weight-bold text-home-title font-medium pb-4',
                                                ),
                                                html.Div(
                                                    [
                                                        html.P(
                                                            """
                                                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
                                                            incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
                                                            exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure 
                                                            dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
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
                            className='row pb-5 pt-5 div-for-alerta',
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
                                            # Table: Alerta: Sobrecosto
                                            "Alerta Transparencia Activa",
                                            className='col my-auto',
                                        ),
                                        html.Div(
                                            # Table: Alerta: Sobrecosto
                                            className='col my-auto buttons-footer-table',
                                            children=[
                                                    dbc.Button("Anterior", id='previous-page', n_clicks=0, className='buttons-footer'), 
                                                    dbc.Button("Siguiente", id='next-page', n_clicks=0, className='buttons-footer'),
                                            ],
                                        ),
                                    ],
                                    className='row mai-datatable-footer'
                                ),                                
                                html.Div (
                                    [
                                        html.Div(
                                            id='table-transparency',
                                            className='table my-0'
                                        ),
                                    ],
                                    className='row mx-0',
                                ),
                                html.Div (
                                    [
                                        html.Div(
                                            # Table: Alerta: Sobrecosto
                                            id='count_entries',
                                            className='col my-auto',
                                        ),
                                        html.Div(
                                            # Table: Alerta: Sobrecosto
                                            className='col my-auto buttons-footer-table',
                                            children=[
                                                    dbc.Button("Anterior", id='previous-page', n_clicks=0, className='buttons-footer'), 
                                                    dbc.Button("Siguiente", id='next-page', n_clicks=0, className='buttons-footer'),
                                            ],
                                        ),
                                    ],
                                    className='row mai-datatable-footer'
                                ),
                            ],
                            className='border-0',
                        ),
                    ],
                    className='row',
                ),
            ],
            className='main-content-table container',
            id="tabla-container",
        ),
    ]
)

MIN_VAL = 0
MAX_VAL = 10
NUM_ENTRIES = 10

# create callback for modifying page layout
@app.callback(
    [Output("table-transparency", "children"),
    Output("count_entries", "children"),
    Output("previous-page", "disabled"),
    Output("next-page", "disabled")], 
    [Input('previous-page', 'n_clicks'),
    Input('next-page', 'n_clicks')])
def update_table(btn_prev, btn_next):

    global MIN_VAL
    global MAX_VAL
    global NUM_ENTRIES
    LEN_DF_COMPLETE = len(df_transparency)


    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'previous-page' in changed_id:
        MIN_VAL = max(0, MIN_VAL-NUM_ENTRIES-1)
        MAX_VAL = min(LEN_DF_COMPLETE, MAX_VAL-NUM_ENTRIES-1)
    elif 'next-page' in changed_id:
        MIN_VAL = max(0, MIN_VAL+NUM_ENTRIES+1)
        MAX_VAL = min(LEN_DF_COMPLETE, MAX_VAL+NUM_ENTRIES+1)

    if 'dropdown-entries' == 10:
        MIN_VAL = MIN_VAL
        MAX_VAL = min(LEN_DF_COMPLETE, MAX_VAL-NUM_ENTRIES-1)

    if MIN_VAL < 1:
        disabled_prev = True
    else:
        disabled_prev = False

    if MAX_VAL == LEN_DF_COMPLETE:
        disabled_next = True
    else:
        disabled_next = False

    df_transparency_subset = df_transparency.iloc[MIN_VAL:MAX_VAL,:]

    table_transparencia = html.Table(
        # Header
        [html.Thead([html.Th(col) for col in df_transparency_subset.columns]) ] +
        # Body
        [html.Tr([
            html.Td(df_transparency_subset.iloc[i][col]) for col in df_transparency_subset.columns
        ]) for i in range(min(len(df_transparency_subset), 20))],
        # className="table border-collapse",
        id='table-transparency',
        style={"overflowY": "scroll"}
    )

    text_entries = 'Showing {} to {} of {} entries'.format(MIN_VAL+1, min(LEN_DF_COMPLETE, MAX_VAL+1), LEN_DF_COMPLETE)
    
    return table_transparencia, text_entries, disabled_prev, disabled_next