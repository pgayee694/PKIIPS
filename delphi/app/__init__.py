from flask import Flask
import logging
from app.model_engine import ModelEngine

global_model_engine = ModelEngine()
logging.basicConfig(format='[%(levelname)s] %(asctime)s (%(module)s): %(message)s')

from app.plugins.distance_plugin import DistanceAnalyzerPlugin
from app.plugins.graph_plugin import GraphPlugin

app = Flask(__name__)

DATA_ANALYZER_PLUGINS = \
[
    # Put data analyzer plugin instances here
    DistanceAnalyzerPlugin(),
    GraphPlugin()
]


for data_analyzer_plugin in DATA_ANALYZER_PLUGINS:
    global_model_engine.add_analyzer(data_analyzer_plugin)

global_model_engine.start()

from app import routes