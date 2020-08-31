import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from importlib import import_module

# app = dash.Dash(
#    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
# )

from app import app
# El llamado de estos modulos tiene que estar DESPUES de que se crea el app.Dash
from apps import alerta_sobrecosto, alerta_transparencia, visor_datos, home_page, metodologia, concentracion
# Alerta transparencia necesita ser cargado despues de que cargue home. Es para que no dependa alerta transaperencia de home.

server = app.server
# app.config.suppress_callback_exceptions = True

# l2 = alerta_transparencia_new.layout

PLOTLY_LOGO = "/assets/Canopy_Black_Transparente-01.png"

navbar_children = dbc.Nav(
    [
        html.Div(
            [       
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    html.Div(
                        [
                            html.Img(src=PLOTLY_LOGO, height="50px"),
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
                                    "Panorama General", 
                                    href="/panorama-general", 
                                    className='text-uppercase btn-link font-weight-bold font-bold px-2'
                                )
                            ],
                            active=True
                        ),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("Sobrecosto", href="/alerta-sobrecosto", className='dropdown-item-nav'),
                                dbc.DropdownMenuItem("Transparencia", href="/alerta-transparencia", className='dropdown-item-nav'),
                                dbc.DropdownMenuItem("Concentración contratistas", href="/concentracion-contratistas", className='dropdown-item-nav'),
                                dbc.DropdownMenuItem("Financiacion campañas", href="/alerta-transparencia", className='dropdown-item-nav'),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Alertas Tempranas",
                            className='text-uppercase btn-link font-bold px-2',
                            style={'margin-bottom':'0 !important'},
                            toggleClassName = 'btn-link font-weight-bold',
                            bs_size='lg',
                        ),
                        dbc.NavLink(
                            "Metodologia", 
                            href="/metodologia", 
                            className='text-uppercase btn-link font-weight-bold font-bold px-2'
                        ),
                        # dbc.NavLink(
                        #     "Quienes somos", 
                        #     href="/visualizacion-datos", 
                        #     className='text-uppercase btn-link font-weight-bold'
                        # ),
                        # dbc.NavLink(
                        #     "Contacto", 
                        #     href="/visualizacion-datos", 
                        #     className='text-uppercase btn-link font-weight-bold'
                        # ),
                    ],
                    className='row ml-5 pt-3'
                ),
            ],
            className='row'
        )
    ],
    className='mx-auto'
)


navbar = dbc.Navbar(
    navbar_children, 
    id='navbar',
    sticky="top"
)


footer = html.Footer(
    [
        html.Div(
            [
                html.Div(
                    [
                        '© Copyright BizLand. MIRAR EL TEMA DE LAS LICENCIAS!!!!'
                    ],
                    className='copyright'
                )
            ],
            className = 'container py-4'
        )
    ],
    style = {'background-color': '#343a40', 'color': '#aaaaaa'}
)

# define page layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh='False'),
        navbar,
        # Column for user controls (SIDE BAR)
        html.Div(
            id="content"
        ),
        footer
    ]
)



# create callback for modifying page layout
@app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return home_page.layout
    if pathname == "/alerta-sobrecosto":
        alerta_sobrecosto.reload_table_counters()
        return alerta_sobrecosto.layout
    if pathname == "/alerta-transparencia":
        alerta_transparencia.reload_table_counters()
        return alerta_transparencia.layout
    if pathname == "/concentracion-contratistas":
        concentracion.reload_table_counters()
        return concentracion.layout
    if pathname == "/panorama-general":
        return visor_datos.layout
    if pathname == "/metodologia":
        return metodologia.layout
        
    # if not recognised, return 404 message
    return html.P("404 - page not found")



# create callback for modifying navbar
@app.callback(Output("navbar", "className"), [Input("url", "pathname")])
def display_navbar(pathname):
    # Navbar yellow if home
    if pathname == "/":
        return 'div-for-nav-yellow'
    # Else navbar white
    return 'div-for-nav-white'


    


if __name__ == "__main__":
    app.run_server()


