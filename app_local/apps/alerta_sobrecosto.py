import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np
import json


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

# Table parameters ------------
PAGE_SIZE = 10
PAGE_SIZE_CONTRATISTAS = 3

# Dash components ---------

# Table
table_sobrecosto = dash_table.DataTable(
    id='table-editing-simple',
    # Data
    columns=(
        [{'id': c, 'name': c, 'type':'text', 'presentation':'markdown'} for c in df_items.columns]
    ),
    data=df_items.to_dict('records'),
    # Table interactivity
    # Table styling
    style_table={
        'overflowX': 'auto',
        'margin': '0',
        'overflowY': 'scroll',
    },
    style_data={
        'border': '0px'
    },
    # Style cell
    style_cell={
        'fontFamily': 'Open Sans',
        'fontSize': '15px',
        'height': '80px',
        'padding': '2px 22px',
        'whiteSpace': 'inherit',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'backgroundColor': 'rgb(49, 48, 47)',
        'boxShadow': '0 0',
        'whiteSpace': 'normal',
        'height': 'auto',
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'
    },
    # Style header
    style_header={
        'backgroundColor': 'rgb(63, 65, 63)',
        'border': '0px'
    },
    # Style filter
    style_filter={
        'fontFamily': 'Open Sans',
        'height': '40px',
        'backgroundColor': 'rgb(217, 217, 217)',
        'color': '#1E1E1E',
    },
    style_data_conditional=[{
        'if': {
            'column_id': 'Alerta de sobrecosto',
            'filter_query': '{Alerta de sobrecosto} = "Si"'
        },
        'color': '#1E1E1E',
        'backgroundColor': '#fecf0e',
    }],
    page_action='native',
    page_size= PAGE_SIZE,
    persistence=True,
    sort_action='native',
    filter_action='native',
)

# Section layout --------------------

layout = html.Div(
    [
        html.Div (
            className='div-for-paragraphs text-secondary',
            children=[
                # Title
                html.Div(
                    [
                        html.H2("Alerta: Sobrecosto"),
                    ],
                    className='text-left p-5'
                ),
                html.Div(
                    [
                        html.P(
                            """
                            En esta sección podrá acceder a los datos sobre alertas en la
                            contratación destinada a atender la emergencia COVID-19 que posean sobrecostos,
                            lo que quiere decir que se está adquiriendo un producto o servicio por encima
                            del precio real.
                            """
                        ),
                        html.P(
                            """
                            Como usuario puede realizar la búsqueda por las siguientes categorías:
                            Ítem - Nombre de la entidad que contrata – Departamento – Municipio –
                            Proveedor seleccionado – Valor del contrato – Precio por Item.


                            """
                        ),
                        html.P(
                            """
                            Para iniciar la búsqueda debe escribir debajo del título de cada columna la palabra clave de interés.
                            Por ejemplo en la columna Ítem: puede buscar elementos como kits de emergencia y le saldrán a nivel
                            nacional los contratos realizados para adquirir este producto.
                            Como otro ejemplo, si desea ver la contratación en su departamento o municipio, puede buscar escribiendo
                            el nombre de su territorio debajo de la columna correspondiente.

                            """
                        ),
                    ],
                    className='text-left p-5'
                ),
            ]
        ),
        html.Div (
            className='div-for-table',
            children=[
                table_sobrecosto,
            ]
        ),
        html.Div (
            className='div-for-paragraphs',
            children=[
                html.H4("""
                    ¡ALGUNOS TIPS PARA LA BÚSQUEDA!
                """),
                html.P(
                    """
                    Para el valor total del contrato puede utilizar los siguientes caracteres
                    para facilitar la búsqueda =, >, >=, <, <=. En ese caso si desea realizar
                    la búsqueda de un contrato mayor a 50.000.000 COP puede escribir >50.000.000.
                    Si desea uno menor o igual a a 100.000.000 COP puede escribir <=100.000.000.
                    """
                ),
            ]
        )
    ]
)