from flask import Blueprint
from flask_restful import Api

from app.api.client.hello import HelloHandler


client_bp = Blueprint('client', __name__, url_prefix='/api_client/v1')
client = Api(client_bp)


client.add_resource(HelloHandler, '/hello')
