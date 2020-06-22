# --------------------
# Dash app 'app.py'
# --------------------

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import plotly.express as px

# from dash.dependencies import Input, Output
from plotly import graph_objs as go
# from plotly.graph_objs import *
from datetime import datetime as dt



app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server

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



# Tab Styles ---------
# PD: This is here and not in style.css because of Dash config.

tabs_styles = {
    'height': '44px',
    'width': '100%'
}
tab_style = {
    'borderTop': '1px solid #31302F',
    'borderBottom': '1px solid #31302F',
    'borderLeft': '1px solid #31302F',
    'borderRight': '1px solid #31302F',
    'padding': '6px',
    'backgroundColor': '#3f413f'
}

tab_selected_style = {
    'borderTop': '1px solid #31302F',
    'borderBottom': '1px solid #31302F',
    'borderLeft': '1px solid #31302F',
    'borderRight': '1px solid #31302F',
    'backgroundColor': '#fecf0e',
    'color': '#31302F',
    'padding': '6px',
}

# Table parameters ------------
PAGE_SIZE = '10'
PAGE_SIZE_CONTRATISTAS = '3'


# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls (SIDE BAR)
                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("dash-logo-new.png")
                        ),
                        html.H3("COVID-19 - ALERTAS DE CONTRATACIÓN"),
                        html.H5("¡Bienvenido!"),
                        html.P(
                            """
                            A través de esta plataforma podrá visualizar los contratos
                            suscritos para atender a la emergencia COVID-19 a nivel nacional y
                            territorial. En las diferentes secciones podrá encontrar alertas en
                            la contratación, estadísticas de la contratación pública y detalles sobre
                            la metodología del Proyecto Canopy.
                            """
                        ),

                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            children=[
                                """Fuentes: [SECOP I](https://www.datos.gov.co/Presupuestos-Gubernamentales/SECOP-I-2020/c82b-7jfi) |
                                [SECOP II](https://www.datos.gov.co/Gastos-Gubernamentales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h) |
                                [Colombia Compra Eficiente](http://colombiacompra.gov.co/transparencia/api)
                                """
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots (RIGHT)
                html.Div(
                    className="nine columns div-for-dash-tables bg-grey",
                    children=[
                        dcc.Tabs(
                            id="tabs-with-classes",
                            value='tab-2',
                            style=tabs_styles,
                        children=[
                            dcc.Tab(
                                label='Alerta: Sobrecosto',
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    html.Div (
                                        className='div-for-paragraphs',
                                        children=[
                                            # Title
                                            html.H2("Alerta: Sobrecosto"),
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
                                        ]
                                    ),
                                    # Table Alertas: Sobrecosto
                                    html.Div (
                                        className='div-for-table',
                                        children=[
                                            dash_table.DataTable(
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
                            ),
                            dcc.Tab(
                                label='Alerta: Transparencia activa',
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    html.Div (
                                        className='div-for-paragraphs',
                                        children=[
                                            # Title
                                            html.H2("Alerta: Falta Transparencia Activa"),
                                            html.P(
                                                """
                                                En esta sección podrá acceder a los datos sobre alertas en la
                                                contratación destinada a atender la emergencia COVID-19 que carezcan
                                                de una publicación adecuada de los ítems a contratar.
                                                Esto genera falencias en la aplicación del principio de proactividad de
                                                ley 1712 de 2014 conocido como el cumplimiento de la Transparencia Activa.

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
                                        ]
                                    ),
                                    html.Div (
                                        # Table: Alerta: Sobrecosto
                                        className='div-for-table',
                                        children=[
                                            dash_table.DataTable(
                                                id='table-editing-simple-2',
                                                # Data
                                                columns=(
                                                    [{'id': c, 'name': c, 'type':'text', 'presentation':'markdown'} for c in df_transparency.columns]
                                                ),
                                                data=df_transparency.to_dict('records'),
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
                                                page_size= PAGE_SIZE,
                                                persistence=True,
                                                sort_action='native',
                                                filter_action='native',
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            dcc.Tab(
                                label='Visor de datos',
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    html.H4('Contratacion para la emergencia de COVID-19 a nivel nacional'),
                                    html.Div (
                                        className='div-for-paragraphs',
                                        children=[
                                            # Title
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
                                        ]
                                    ),
                                    html.Div(
                                        className="div-for-map",
                                        children=[
                                            dcc.Graph(figure=fig_map_2),
                                        ]
                                    ),
                                    # html.Div(
                                    #     className="div-for-dropdown",
                                    #     children=[
                                    #         dcc.Dropdown(
                                    #             id='bar-plot-dropdown-municipios',
                                    #             options=[{'label': i, 'value': i} for i in entidades_items],
                                    #             value='Municipio'
                                    #         ),
                                    #     ]
                                    # ),
                                    html.H4('Concentracion de proveedores a nivel regional'),
                                    html.Div (
                                        className='div-for-paragraphs',
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
                                    html.Div(
                                        className="six columns div-for-bar-chart",
                                        children=[
                                            dcc.Graph(id = 'bar-plot-items', figure = fig)
                                        ]
                                    ),
                                    html.Div(
                                        className="six columns div-for-bar-chart",
                                        children=[
                                            dash_table.DataTable(
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
                                                    'overflowY': 'scroll',
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
                                        ]
                                    ),
                                ]
                            )

                        ])
                    ]
                )
            ]
        )
    ]
)


# Interactivity -------------------
#
# @app.callback(
#     dash.dependencies.Output('bar-plot-items', 'figure'),
#     [dash.dependencies.Input('bar-plot-dropdown-municipios', 'value')])
# def update_graph(dropdown_municipios):
#     dff = df_items[df_items['Municipio'] == dropdown_municipios]
#     grouped_dff = dff.groupby('Descripción del item').size().reset_index(name='Numero de contratos').sort_values(by='Numero de contratos', ascending=False)
#
#     trace_1 = go.Bar(y=animals, x=[10, 5, 4], orientation='h')
#     fig = go.Figure(data = [trace_1], layout = layout)
#     return fig



if __name__ == "__main__":
    app.run_server(debug=True)
