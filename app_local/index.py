import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app
from importlib import import_module

app.title = 'Recidivism analysis'

server = app.server

#Loading menu from json file
with open('data/menu.json', encoding='utf-8') as response:
    menu = json.load(response)

#Building menu
num_links=0
def get_next_link_id(item):
    global num_links
    num_links += 1
    item['id'] = f'btn-{num_links}'
    return item['id']

hash_path = []
nav_items = []
submenus = []
for item in menu:
    collapse_items = None
    item_id = get_next_link_id(item)
    if 'items' in item :
        submenus.append(f'submenu-{num_links}')
        collapse_items = dbc.Collapse(
            html.Div(
                [
                    html.A(
                        subitem['label'],
                        className='collapse-item',
                        id=get_next_link_id(subitem),
                        href=subitem['path']
                    )
                    for subitem in item['items']
                ],
                className='bg-white py-2 collapse-inner rounded',
            ),
            id=submenus[-1],
        )    
    nav_items.append(
        dbc.NavItem([
            dbc.NavLink(
                [ html.I(className=item['class']), ' '+item['label'] ],
                id=item_id,                                      
                href=item['path']
            ),
            collapse_items
        ]),
    )

#Main container
container = html.Div(
    [
        dbc.Row(
            [
                dbc.Collapse(
                    [
                        html.Div(
                            dbc.Nav(
                                nav_items,
                                className="flex-column",
                            ),
                            className="sidebar-sticky pt-3",
                        )                     
                    ],
                    id="sidebarMenu",
                    className="col-md-3 col-lg-2 d-md-block bg-light sidebar",
                    navbar=True
                ),
                html.Main(
                    id='page-content',
                    className="col-md-9 ml-sm-auto col-lg-10 px-md-4",
                    role="main",
                )
            ]
        )
    ],
    className="container-fluid",
)

#Navbar
navbar = dbc.Navbar(
    [
        html.A(
            'Team 86',
            href="/",
            className="navbar-brand col-md-3 col-lg-2 mr-0 px-3"
        ),
        dbc.Row(
            [
                #dbc.Col(html.Img(src='/assets/img/icon.png', height="30px"), className='text-right'),
                dbc.Col(dbc.NavbarBrand("Recidivism analysis", className="ml-2", id="brand-title")),
            ],
            align="center",
            no_gutters=True,
            className="d-none d-md-flex"
        ),
        dbc.NavbarToggler(id="navbar-toggler", className="position-absolute d-md-none"),
        
    ],
    color="dark",
    dark=True,
    className="sticky-top shadow p-0",
)

#Create Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    container
])

#callbacks
# add callback for toggling the collapse on small screens
@app.callback(
    Output("sidebarMenu", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("sidebarMenu", "is_open")],
)
def toggle_sidebarMenu(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output(f"submenu-{i}", "is_open") for i in [2]],
    [Input(f"btn-{i}", "n_clicks") for i in [2]],
    [State(f"submenu-{i}", "is_open") for i in [2]]
)
def toggle_submenu(*args):
    status = []
    num_buttons = int(len(args)/2)
    for i in range(0, num_buttons):
        n = args[i]
        is_open = args[i+num_buttons]
        status.append(n and n%2 == 1)
    return status


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    for item in menu:
        if pathname == item['path']:
            return import_module(item['module']).layout

        if 'items' in item :
            for subitem in item['items']:
                if 'module' in subitem and pathname == subitem['path']:
                    return import_module(subitem['module']).layout
    return '404'

@app.callback([Output(f"btn-{i}", "className") for i in range(1, num_links+1)],
              [Input('url', 'pathname')])
def set_active(pathname):
    actives = []
    
    for item in menu:
        i = len(actives)
        if pathname == item['path']:
            actives.append('active')
        else :
            actives.append('')

        if 'items' in item :
            for subitem in item['items']:
                if pathname == subitem['path']:
                    actives.append('collapse-item active')
                    actives[i] = 'active'
                else :
                    actives.append('collapse-item')

    return actives

#Initiate endhe server where the app will work
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=5000)