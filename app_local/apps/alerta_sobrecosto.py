import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np

from data import df_items, entidades_items


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
                                                    'Alerta: Sobrecosto', 
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
            className='div-for-table',
            children=[
                table_sobrecosto,
            ]
        ),
    ]
)