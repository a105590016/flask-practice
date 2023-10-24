from flask import Blueprint
import importlib, pathlib

application = app = Blueprint('myapp_v1', __name__)

endpoints = pathlib.Path(__file__).resolve().parent

for endpoint in pathlib.Path(f"{endpoints}/endpoints").glob('**/*.py'):
    endpoint = str(endpoint).replace(str(pathlib.Path.cwd()), '')
    endpoint = endpoint[1:-3].replace('/', '.')
    importlib.import_module(endpoint)