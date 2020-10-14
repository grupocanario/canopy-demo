import dash

metas = [{
    "name": "viewport", 
    "content": "width=device-width",
    "og:title": "Proyecto Canopy",
    "og:description": "Alertas tempranas para la contratación pública de COVID-19 en Colombia.",
    "og:image": "https://raw.githubusercontent.com/grupocanario/canopy-demo/master/app_local/assets/logos/bird.png",
    "og:url": "https://www.proyectocanopy.co/"
}]

app = dash.Dash(
    __name__, 
    meta_tags=metas, 
    title='Canopy',
    update_title='Cargando...',
    suppress_callback_exceptions=True
)