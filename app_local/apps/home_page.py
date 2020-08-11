import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np
import json


# Section layout --------------------

layout = html.Div(
    [
        html.Div( 
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1('Punny Headline', className='display-4 font-weight-normal text-dark'),
                            ],
                            className='mb-5',
                        ),
                        html.Div(
                            [
                                html.P(
                                    """And an even wittier subheading to boot. 
                                    Jumpstart your marketing efforts with this example based on Apple's marketing pages.""", 
                                    className='lead font-weight-normal text-dark font-home-m'
                                ),
                            ],
                            className='mb-5',
                        ),
                        html.Div(
                            [
                                html.A('Coming soon', className='btn btn-outline-secondary text-dark font-home-m', href="#"),
                            ]
                        ),
                    ],
                    className='col-md-5 p-lg-5 mx-auto my-5',
                ),
            ],
            className = 'position-relative overflow-hidden text-center',
            style = {'background-color': '#FFD608'}
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2('Fuentes de datos', className='display-4 font-weight-normal text-dark')
                            ],
                            className='mb-5 border-bottom-yellow',
                        ),
                        html.Div(
                            [
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.P("SECOP I", className="lead card-sources-text px-3")
                                        ]
                                    ),
                                    style={"width": "18rem"},
                                    className='mx-auto'
                                )
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.P("SECOP I", className="lead card-sources-text px-3")
                                                ]
                                            ),
                                            style={"width": "18rem"},
                                            className = 'mx-4',
                                        ), 
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.P("SECOP I", className="lead card-sources-text px-3")
                                                ]
                                            ),
                                            style={"width": "18rem"},
                                            className = 'mx-4',
                                        ), 
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.P("SECOP I", className="lead card-sources-text px-3")
                                                ]
                                            ),
                                            style={"width": "18rem"},
                                            className = 'mx-4',
                                        )
                                    ],
                                    className = 'mx-auto'
                                )
                            ],
                            className='my-5',
                        ),
                        html.Div(
                            [
                                html.A('Coming soon', className='btn btn-outline-secondary text-dark font-home-m', href="#"),
                            ]
                        ),
                    ],
                    className = 'col-md-5 p-lg-5 mx-auto my-5'
                ),
            ],
            className = 'position-relative overflow-hidden text-center',
        )
    ]
)