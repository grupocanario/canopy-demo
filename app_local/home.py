import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import alerta_sobrecosto, alerta_transparencia, visor_datos
from importlib import import_module


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

    #     dbc.Row(
    #         [       
    #             html.A(
    #                 # Use row and col to control vertical alignment of logo / brand
    #                 dbc.Row(
    #                     [
    #                         dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
    #                     ]
    #                 ),
    #                 href="https://plot.ly",
    #             ),
    #             dbc.NavItem(dbc.NavLink("Page 1", href="/page-1")),
    #             dbc.NavItem(dbc.NavLink("Page 2", href="/page-2")),
    #             dbc.NavItem(dbc.NavLink("Page 3", href="/page-3")),
    #         ],
    #     )
    # ],
    # className='mx-auto'
    
navbar_children = dbc.Nav(
    [
        html.Div(
            [       
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    html.Div(
                        [
                            html.Img(src=PLOTLY_LOGO, height="30px"),
                        ],
                        className='mr-5',
                    ),
                    href="https://plot.ly",
                ),
                html.Div(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                "Visualizacion de datos", 
                                href="/visualizacion-datos", 
                                className='text_menu text-uppercase'
                            )
                        ),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("Sobrecosto", href="/alerta-sobrecosto"),
                                dbc.DropdownMenuItem("Transparencia", href="/alerta-transparencia"),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Alertas Tempranas",
                            className='text_menu text-uppercase',
                            style={'margin-bottom':'0 !important'}
                        ),
                        # dbc.NavItem(
                        #     dbc.NavLink(
                        #         "Metodologia", 
                        #         href="/visualizacion-datos", 
                        #         className='text_menu text-uppercase'
                        #     ),
                        #     style={'margin-bottom':'0 !important'}
                        # ),
                        # dbc.NavItem(
                        #     dbc.NavLink(
                        #         "Quienes somos", 
                        #         href="/visualizacion-datos", 
                        #         className='text_menu text-uppercase'
                        #     )
                        # ),
                        # dbc.NavItem(
                        #     dbc.NavLink(
                        #         "Contacto", 
                        #         href="/visualizacion-datos", 
                        #         className='text_menu text-uppercase'
                        #     )
                        # ),
                        dbc.NavLink(
                            "Metodologia", 
                            href="/visualizacion-datos", 
                            className='text_menu text-uppercase'
                        ),
                        dbc.NavLink(
                            "Quienes somos", 
                            href="/visualizacion-datos", 
                            className='text_menu text-uppercase'
                        ),
                        dbc.NavLink(
                            "Contacto", 
                            href="/visualizacion-datos", 
                            className='text_menu text-uppercase'
                        ),
                    ],
                    className='row ml-5'
                ),
            ],
            className='row'
        )
    ],
    className='mx-auto'
)


navbar = dbc.Navbar(
    navbar_children, 
    sticky="top",
    className='div-for-nav'
)


# define page layout
app.layout = html.Div(
    [
        dcc.Location(id="url", pathname="/page-1"),
        navbar,
        # Column for user controls (SIDE BAR)
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="three columns div-user-controls bg-grey",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("dash-logo-new.png")
                        ),
                        html.Div(
                            [ 
                                html.H3("COVID-19 - ALERTAS DE CONTRATACIÓN"),
                            ],
                            className='pb-5'
                        ),
                        html.Div(
                            [ 
                                html.P(
                                    """
                                    A través de esta plataforma podrá visualizar los contratos
                                    suscritos para atender a la emergencia COVID-19 a nivel nacional y
                                    territorial. En las diferentes secciones podrá encontrar alertas en
                                    la contratación, estadísticas de la contratación pública y detalles sobre
                                    la metodología del Proyecto Canopy.
                                    """
                                ),
                            ],
                            className='pt-3 pb-5'
                        ),
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
                dbc.Container(
                    id="content"
                ),
            ]
        )
    ]
)



# create callback for modifying page layout
@app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/alerta-sobrecosto":
        return alerta_sobrecosto.layout
    if pathname == "/alerta-transparencia":
        return alerta_transparencia.layout
    if pathname == "/visualizacion-datos":
        return visor_datos.layout
    # if not recognised, return 404 message
    return html.P("404 - page not found")


if __name__ == "__main__":
    app.run_server()
