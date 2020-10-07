# --------------------
# Copyright (c) 2020 Grupo Canario

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table


layout = html.Div(
    [

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                "Metodología",
                                className = 'mx-auto title-visor',
                                style={'display': 'inline-block'}
                                ),
                            ],
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
                            En esta sección podrás revisar la información sobre la metodología de trabajo llevado a cabo por nuestro equipo para cada alerta. Te invitamos a revisar esta información si quieres saber más sobre el proceso llevado a cabo por Canopy para facilitar una veeduría ciudadana frente a los contratos adjudicados por la emergencia del Covid-19. 
                            """,
                        ),
                    ],
                    className='px-8 mb-5 pb-5 text-center lead'
                ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    """
                                    Alerta sobrecosto
                                    """,
                                    className='col-4 titles-metodologia text-center align-self-center'
                                ),
                                html.Div(
                                    html.P(
                                        """
                                        En esta alerta comparamos los precios de los Acuerdos Marco encontrados en Colombia Compra Eficiente del COVID-19 como precios de referencia de mercado, y los comparamos con el valor del precio unitario de los contratos en el SECOP II. La información extraída de SECOP II para hacer la comparación de precio unitario en el contrato es el número de ítems/valor total del contrato.
                                        """,
                                        
                                    ),
                                    className='col'
                                )
                            ],
                            className='row px-8 lead'
                        ),
                    ],
                    className='py-6', 
                    style={'background-color': '#F9E178'}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    """
                                    Alerta transparencia    
                                    """,
                                    className='col-4 titles-metodologia text-center align-self-center'
                                ),
                                html.Div(
                                    html.P(
                                        """
                                        Extraemos la información de la API de OCDS y revisamos la categoría de tender y el campo de ítems, para ver la clasificación de los bienes o servicios del contrato. En caso de que el contrato no cuente con una clasificación clara del contrato, se reporta una alarma de transparencia.
                                        """,
                                        
                                    ),
                                    className='col'
                                )
                            ],
                            className='row px-8 lead'
                        ),
                    ],
                    className='py-6', 
                    style={'background-color': '#8989892e'}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    """
                                    Alerta concentración de contratistas
                                    """,
                                    className='col-4 titles-metodologia text-center align-self-center'
                                ),
                                html.Div(
                                    html.P(
                                        """
                                        Tomamos la información de SECOP I y II y agregamos por los campos de departamento, nit_contratista y valor total del contrato. Posteriormente, dividimos el valor resultante para cada contratista sobre el valor total contratado para el respectivo departamento.
                                        """,
                                        
                                    ),
                                    className='col'
                                )
                            ],
                            className='row px-8 lead'
                        ),
                    ],
                    className='py-6', 
                    style={'background-color': '#F9E178'}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    """
                                    Alerta financiación de campañas
                                    """,
                                    className='col-4 titles-metodologia text-center align-self-center'
                                ),
                                html.Div(
                                    html.P(
                                        """
                                        Realizamos la comparación de la base de datos obtenida del visor ciudadano de Transparencia por Colombia [https://www.monitorciudadano.co/elecciones-contratos/descargas] sobre los financiadores de campañas políticas y la cruzamos con el nit_contratista de la base de datos del SECOP I y II obtenida de la API en el estándar OCDS. Reportamos entonces la información sobre el contratista, el contrato y el político al que realizó la financiación.
                                        """,
                                        
                                    ),
                                    className='col'
                                )
                            ],
                            className='row px-8 lead'
                        ),
                    ],
                    className='py-6', 
                    style={'background-color': '#8989892e'}
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            """
                            Adicionalmente, puede encontrar todo el código fuente del proyecto Canopy en GitHub
                            """,
                        ),
                        html.A(
                            [
                                html.Div(
                                    [
                                        html.Img(src='/../assets/logos/github.png', className='div-for-image-github')
                                    ],
                                ),
                            ],
                            href='https://github.com/grupocanario/canopy',
                        ),
                        html.P(
                            """
                            Para cualquier duda adicional, por favor comunicarse al correo
                            """,
                            className='pt-5',
                        ),
                        html.Div(
                            'proyectocanopy@gmail.com', 
                            className='row mx-auto justify-content-center pt-2 text-mail-contact',
                        ),
                    ],
                    className='px-8 my-5 py-5 text-center lead'
                ),
            ],
        ),
    ]
)