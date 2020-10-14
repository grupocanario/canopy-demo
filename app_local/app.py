import dash

metas = [
    {"name": "viewport", "content": "width=device-width"},
    {"property": "og:title", "content": "Proyecto Canopy"}, 
    {"property": "og:description", "content": "Monitoreo de la contratación pública de COVID-19 en Colombia por medio de visualizaciones y alertas tempranas."}, 
    {"property": "og:image", "content": "https://raw.githubusercontent.com/grupocanario/canopy-demo/master/canopy_thumbnail.png"}, 
    {"property": "og:url", "content": "https://www.proyectocanopy.co/"}
]

app = dash.Dash(
    __name__, 
    meta_tags=metas, 
    title='Canopy',
    update_title='Cargando...',
    suppress_callback_exceptions=True
)