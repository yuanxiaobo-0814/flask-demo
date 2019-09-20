from flask import Blueprint
from flask_restful import Api

from app.api.admin.user import UserHandler

admin_bp = Blueprint('admin', __name__, url_prefix='/api_admin/v1')
admin = Api(admin_bp)


admin.add_resource(UserHandler, '/user')
