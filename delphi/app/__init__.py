from flask import Flask
from app.model_engine import ModelEngine

app = Flask(__name__)

DATA_ANALYZER_PLUGINS = \
[
    # Put data analyzer plugin instances here
]

global_model_engine = ModelEngine()
for data_analyzer_plugin in DATA_ANALYZER_PLUGINS:
    global_model_engine.add_analyzer(data_analyzer_plugin)

global_model_engine.start()

from app import routes