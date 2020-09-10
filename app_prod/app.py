
# --------------------
# Flask
# --------------------
from flask import Flask

server = Flask(__name__)

# --------------------
# Dash app 'app.py'
# --------------------

import dash

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server