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
                            'BIENVENIDOS A CANOPY', 
                            className='mb-5 display-4 font-weight-bold text-home-title font-medium',
                        ),
                        html.Div(
                            [
                                html.P(
                                    """
                                    Esta es una plataforma creada para facilitar la veeduría ciudadana sobre los contratos que ha adjudicado el Gobierno de Colombia para la emergencia del COVID-19.
                    
                                    """, 
                                    className='lead font-weight-normal text-dark font-home-m'
                                ),

                                html.P(
                                    """
                                    
                                    Navega entre las alertas tempranas que hemos creado para explorar cómo están funcionando las contrataciones a lo largo del país. 
                                    """, 
                                    className='lead font-weight-normal text-dark font-home-m'
                                ),
                            ],
                            className='mb-5',
                        ),
                        html.Div(
                            [
                                html.A('Comenzar a explorar', className='btn btn-outline-secondary text-dark font-home-m', href="/panorama-general"),
                            ]
                        ),
                    ],
                    className='col-md-5 p-lg-5 mx-auto my-5',
                ),
            ],
            className = 'position-relative overflow-hidden text-center back-home',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            'NUESTROS ALIADOS', 
                            className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                        ),
                        html.Div(
                            'Las siguientes organizaciones apoyan el proyecto Canopy', 
                            className='row mx-auto justify-content-center text-home-paragraph',
                        ),
                        html.Div(
                            [
                                html.A(
                                    [
                                        html.Div(
                                            [
                                                html.Img(src='/../assets/logos/ocp.png', className='div-for-image-ocp')
                                            ],
                                            className='col'
                                        ),
                                    ],
                                    href="https://www.open-contracting.org/es/",
                                ),
                                html.A(
                                    [
                                        html.Div(
                                            [
                                                html.Img(src='/../assets/logos/british-embassy.jpg', className='div-for-image-embassy')
                                            ],
                                            className='col'
                                        ),
                                    ],
                                    href="https://www.gov.uk/world/organisations/british-embassy-colombia.es-419",
                                ),
                                html.A(
                                    [
                                        html.Div(
                                            [
                                                html.Img(src='/../assets/logos/secretaria_transparencia.png', className='div-for-image-secretaria')
                                            ],
                                            className='col'
                                        ),
                                    ],
                                    href="http://www.secretariatransparencia.gov.co/",
                                ),
                            ],
                            className='row align-items-center justify-content-center'
                        ),
                    ],
                    className = 'container pt-5 mt-2'
                ),

                html.Div(
                    [
                        html.Div(
                            'FUENTES DE DATOS', 
                            className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                        ),
                        html.Div(
                            'Estas son las principales fuentes para la elaboracion de este proyecto', 
                            className='row mx-auto justify-content-center text-home-paragraph',
                        ),
                        html.Div(
                            [
                                html.A(
                                    [
                                        html.Div(
                                            [
                                                html.Img(src='/../assets/logos/OCDS-logo.png', className='div-for-image-ocds')
                                            ],
                                            className='col'
                                        ),
                                    ],
                                    href='https://www.open-contracting.org/data-standard/',
                                ),
                                html.A(
                                    [
                                        html.Div(
                                            [
                                                html.Img(src='/../assets/logos/SECOP-1.png', className='div-for-image-secop-i')
                                            ],
                                            className='col'
                                        ),
                                    ],
                                    href='https://www.colombiacompra.gov.co/secop/secop-i',
                                ),
                                html.A(
                                    [
                                        html.Div(
                                            [
                                                html.Img(src='/../assets/logos/SECOP-1.png', className='div-for-image-secop-i')
                                            ],
                                            className='col'
                                        ),
                                    ],
                                    href='https://www.colombiacompra.gov.co/secop-ii',
                                ),
                                html.A(
                                    [
                                        html.Div(
                                            [
                                                html.Img(src='/../assets/logos/colombia-compra-eficiente.png', className='div-for-image-compra-eficiente')
                                            ],
                                            className='col'
                                        ),
                                    ],
                                    href='https://www.colombiacompra.gov.co/',
                                ),
                            ],
                            className='row align-items-center justify-content-center pl-2'
                        ),
                    ],
                    className = 'container pt-4 mb-5',
                ),
            ],
            className = 'position-relative overflow-hidden text-center',
            id='aliados'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            'QUIENES SOMOS', 
                            className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                        ),
                        html.Div(
                            'El equipo detrás del proyecto Canopy', 
                            className='row mx-auto justify-content-center text-home-paragraph',
                        ),
                    ],
                    className = 'container pt-5 mt-2'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(src='/../assets/fotos_team/david.jpeg', className='div-for-image-team'),
                                        html.Div('David Gamba', className='font-weight-bold text-names-team font-medium'),
                                        html.Div('Data Scientist', className='text-subtitle-team'),
                                        html.Div('''
                                        Magni qui quod omnis unde et eos fuga et exercitationem. Odio veritatis perspiciatis quaerat qui aut aut aut 
                                        ''', className= 'text-description-team'
                                        ),
                                        html.Div(
                                            html.A(
                                                html.I(className="fab fa-linkedin", style={'color': 'grey'}), 
                                                href='https://www.linkedin.com/in/cdavidgamba/', role="button",
                                            ),
                                            className='social',                                        
                                        ),
                                    ],
                                    className='col div-for-member mx-4', 
                                ),
                                html.Div(
                                    [
                                        html.Img(src='/../assets/fotos_team/melissa.jpeg', className='div-for-image-team'),
                                        html.Div('Melissa Montes Martin', className='font-weight-bold text-names-team font-medium'),
                                        html.Div('Data Scientist', className='text-subtitle-team'),
                                        html.Div('''
                                        Magni qui quod omnis unde et eos fuga et exercitationem. Odio veritatis perspiciatis quaerat qui aut aut aut 
                                        ''', className= 'text-description-team'
                                        ),
                                        html.Div(
                                            html.A(
                                                html.I(
                                                    className="fab fa-linkedin", style={'color': 'grey'}), 
                                                    href='https://www.linkedin.com/in/melissa-montes-martin/', role="button",
                                            ),
                                            className='social',                                        
                                        ),
                                    ],
                                    className='col div-for-member mx-4', 
                                ),
                                html.Div(
                                    [
                                        html.Img(src='/../assets/fotos_team/carlos.jpeg', className='div-for-image-team'),
                                        html.Div('Carlos Caro', className='font-weight-bold text-names-team font-medium'),
                                        html.Div('Data Scientist', className='text-subtitle-team'),
                                        html.Div('''
                                        Magni qui quod omnis unde et eos fuga et exercitationem. Odio veritatis perspiciatis quaerat qui aut aut aut 
                                        ''', className= 'text-description-team'
                                        ),
                                        html.Div(
                                            html.A(
                                                html.I(
                                                    className="fab fa-linkedin", style={'color': 'grey'}), 
                                                    href='https://www.linkedin.com/in/carloscaro/', role="button",
                                            ),
                                            className='social',                                        
                                        ),
                                    ],
                                    className='col div-for-member mx-4', 
                                ),
                            ],
                            className='row',
                        ),
                    ],
                    className = 'container pt-5 mt-2 mb-5 d-flex justify-content-center'
                ),
            ],
            className = 'position-relative overflow-hidden text-center div-for-quienes-somos',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            'CONTACTO', 
                            className='row mb-2 display-4 font-weight-bold text-home-title mx-auto justify-content-center font-medium',
                        ),
                        html.Div(
                            'Para mas información por favor comuníquese al correo', 
                            className='row mx-auto justify-content-center pt-4 text-home-paragraph',
                        ),
                        html.Div(
                            'proyectocanopy@gmail.com', 
                            className='row mx-auto justify-content-center pt-3 text-mail-contact',
                        ),
                    ],
                    className = 'container py-5 mt-2'
                ),
            ],
            className = 'position-relative overflow-hidden text-center pb-2',
        ),
    ]
)