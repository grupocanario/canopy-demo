import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import alerta_sobrecosto, alerta_transparencia, visor_datos, home_page
from importlib import import_module


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server

PLOTLY_LOGO = "/assets/Canopyblack.png"

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
                    href="/",
                ),
                html.Div(
                    [
                        dbc.NavItem(
                            [
                                dbc.NavLink(
                                    "Visualizacion de datos", 
                                    href="/visualizacion-datos", 
                                    className='text-uppercase btn-link font-weight-bold'
                                )
                            ],
                            active=True
                        ),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("Sobrecosto", href="/alerta-sobrecosto"),
                                dbc.DropdownMenuItem("Transparencia", href="/alerta-transparencia"),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Alertas Tempranas",
                            className='text-uppercase btn-link font-weight-bold',
                            style={'margin-bottom':'0 !important'},
                            toggleClassName = 'btn-link font-weight-bold',
                            bs_size='lg',
                        ),
                        dbc.NavLink(
                            "Metodologia", 
                            href="/visualizacion-datos", 
                            className='text-uppercase btn-link font-weight-bold'
                        ),
                        dbc.NavLink(
                            "Quienes somos", 
                            href="/visualizacion-datos", 
                            className='text-uppercase btn-link font-weight-bold'
                        ),
                        dbc.NavLink(
                            "Contacto", 
                            href="/visualizacion-datos", 
                            className='text-uppercase btn-link font-weight-bold'
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
        dcc.Location(id="url", pathname="/"),
        navbar,
        # Column for user controls (SIDE BAR)
        html.Div(
            id="content"
        ),
    ]
)



# create callback for modifying page layout
@app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return home_page.layout
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
