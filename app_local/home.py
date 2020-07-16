import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import alerta_sobrecosto, alerta_transparencia, visor_datos
from importlib import import_module

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar_children = [
    dbc.NavItem(dbc.NavLink("Page 1", href="/page-1")),
    dbc.NavItem(dbc.NavLink("Page 2", href="/page-2")),
    dbc.NavItem(dbc.NavLink("Page 3", href="/page-3")),
]

navbar = dbc.Navbar(navbar_children, sticky="top")


# define content for page 2

page2 = html.Div (
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
)

# define page layout
app.layout = html.Div(
    [
        dcc.Location(id="url", pathname="/page-1"),
        navbar,
        dbc.Container(id="content", style={"padding": "20px"}),
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
