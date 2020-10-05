import dash

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}], 
    title='Canopy',
    update_title='Cargando...',
    suppress_callback_exceptions=True
)