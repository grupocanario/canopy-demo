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

navbar_children = [
    dbc.NavItem(dbc.NavLink("Page 1", href="/page-1")),
    dbc.NavItem(dbc.NavLink("Page 2", href="/page-2")),
    dbc.NavItem(dbc.NavLink("Page 3", href="/page-3")),
]

navbar = dbc.Navbar(navbar_children, sticky="top")


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
    if pathname == "/page-1":
        return alerta_sobrecosto.layout
    if pathname == "/page-2":
        return alerta_transparencia.layout
    if pathname == "/page-3":
        return visor_datos.layout
    # if not recognised, return 404 message
    return html.P("404 - page not found")


if __name__ == "__main__":
    app.run_server()
