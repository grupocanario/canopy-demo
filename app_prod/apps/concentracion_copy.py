import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np
import json
from urllib.request import urlopen
import plotly.express as px
from plotly import graph_objs as go

# DATAFRAMES -----------------

# 3. Dataframe SECOP I & II map (number of COVID contracts)
df_raw_covid = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/secop_all_is_covid.csv")

df_covid = df_raw_covid.copy()
df_national_covid = df_covid.groupby('departamento').size().reset_index(name='Numero de contratos COVID')
df_national_covid = df_national_covid.rename(columns={'departamento':'Departamento'})
df_national_covid['Departamento_upper'] = df_national_covid['Departamento'].str.upper()

df_codes = pd.read_csv("https://raw.githubusercontent.com/melissamnt/code_utils/master/csv_department_codes.csv",
                   dtype={"cod": str})
df_codes['Code'] = df_codes['Code'].astype('str')
df_codes = df_codes.replace({'5': '05', '8': '08'})
df_national_covid = pd.merge(df_national_covid, df_codes, left_on='Departamento_upper',  right_on='Departamento', how='left')
df_national_covid = df_national_covid.rename(columns={'Departamento_x':'Departamento'}).drop(['Departamento_upper', 'Departamento_y'], axis=1)

# 4. Dataframe SECOP I & II concentracion top 10 contratistas por depto
df_raw_proov_cum = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/cum_dept_valor.csv")
df_proov_cum = df_raw_proov_cum.rename(columns={'0':'Departamento', '1': 'Pct proveedores'})
df_proov_cum = df_proov_cum.drop('Unnamed: 0', axis=1)
df_proov_cum = df_proov_cum.sort_values(by='Pct proveedores', ascending=True)

# 5. Dataframe SECOP I & II nombre de top 10 contratistas por depto
df_raw_proov = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/prov_dept_valor.csv")
df_proov = df_raw_proov.rename(columns={'documento_proveedor':'Documento proveedor',
    'departamento': 'Departamento',
    'valor_del_contrato': 'Valor del contrato',
    'tipodocproveedor': 'Tipo documento proveedor',
    'proveedor_adjudicado': 'Proveedor adjudicado'})
df_proov = df_proov.drop('Unnamed: 0', axis=1)


# GRAPHS ----------------------

# 1. Colombia cloropleth map: Number of contracts per department

with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json') as response:
    departments = json.load(response)

fig_map_2 = px.choropleth_mapbox(df_national_covid,
                           geojson=departments,
                           locations='Code',
                           color='Numero de contratos COVID',
                           featureidkey='properties.DPTO',
                           hover_name='Departamento',
                           color_continuous_scale="Viridis",
                           range_color=(0, max(df_national_covid['Numero de contratos COVID'])),
                           mapbox_style="carto-positron",
                           zoom=4,
                           center = {"lat": 4.570868, "lon": -74.2973328},
                           opacity=0.5
                          )
fig_map_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



# 2. Top 10 contratistas Bar plot

trace_1 = go.Bar(x=df_proov_cum['Pct proveedores'], y=df_proov_cum['Departamento'], orientation='h')

layout = go.Layout(title = 'Time Series Plot',
                   hovermode = 'closest')
fig = go.Figure(data = [trace_1], layout = layout)
fig.update_layout(
    title={
        'text': "% presupuesto adjudicado a top 10 contratistas",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    # margin=go.layout.Margin(l=10, r=0, t=0, b=50),
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font=dict(
        color="#f2f2f2",
        family="Open Sans"
    )
)

# TABLES -----------
PAGE_SIZE_CONTRATISTAS = 3

table_contractors = dash_table.DataTable(
    id='table-editing-simple-3',
    # Data
    columns=(
        [{'id': c, 'name': c, 'type':'text', 'presentation':'markdown'} for c in df_proov.columns]
    ),
    data=df_proov.to_dict('records'),
    # Table interactivity
    # Table styling
    style_table={
        'overflowX': 'auto',
        'margin': '0',
        'overflowY': 'auto',
    },
    style_data={
        'border': '0px'
    },
    # Style cell
    style_cell={
        'fontFamily': 'Open Sans',
        'height': '60px',
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
        'fontColor': 'black',
    },
    # style_data_conditional=[{
    #     'if': {
    #         'column_id': 'Alerta de sobrecosto',
    #         'filter_query': '{Alerta de sobrecosto} = "Alerta"'
    #     },
    #     'fontColor': 'black',
    #     'backgroundColor': '#ffb575',
    # }],
    page_action='native',
    page_size= PAGE_SIZE_CONTRATISTAS,
    persistence=True,
    sort_action='native',
    filter_action='native',
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
                                    'Visualización de datos', 
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
                                    En esta sección podrá visualizar el número de contratos
                                    que se han realizado para atender a la emergencia COVID19
                                    por departamento. Para conocer el número, dirija el cursor
                                    a cada departamento en el mapa.
                                    """
                                ),
                                html.P(
                                    """
                                    La siguiente gráfica le indica los departamentos donde
                                    se encuentra la mayor concentración del presupuesto, para atender
                                    la emergencia COVID, en unos pocos contratistas.
                                    """
                                ),
                            ],
                            className='text-left pl-5 pr-5'
                        ),
                    ],
                    className='col',
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                # Title
                                dcc.Graph(figure=fig_map_2)
                            ],
                        ),
                    ],
                    className='p-6 col shadow-sm border-0',
                ),
            ],
            className="row text-secondary",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [   
                                        dcc.Graph(id = 'bar-plot-items-1', figure = fig)
                                    ]
                                )
                            ],
                            className='col shadow-sm border-0',
                        ),
                    ],
                    className='col m-3'
                ),                                            
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4('Concentracion de proveedores a nivel regional'),
                            ],
                            className='text-left p-5'
                        ),
                        html.Div (
                            className='text-left pl-5 pr-5',
                            children=[
                                # Title
                                html.P(
                                    """
                                    Para consultar los datos de los 10 contratistas que concentran
                                    la adjudicación de contratos por departamento, puede acceder a
                                    ellos en la siguiente tabla. Al aplicar el filtro de interés podrá
                                    consultar nombre del contratista, NIT o C.C, valor total del contrato
                                    y departamento correspondiente.
                                    """
                                )
                            ]
                        ),
                    ],
                    className='col'
                ),
            ],
            className='row text-secondary'   
        ),
        html.Div(
            [
                html.Div(
                    className="m-3",
                    children=[
                        table_contractors
                    ]
                ),
            ],
            className='row'   
        )    
    ]
)