from flask_jwt_extended import jwt_required
from flask_restx import marshal_with

from app.main import container
from app.core.presentation.v1.helpers import AbstractResource, ResultEnum, ResultField


class Check(AbstractResource):
    resource_fields = {
        'status': ResultField
    }

    @jwt_required()
    @marshal_with(fields=resource_fields, skip_none=True)
    def post(self):
        return {'status': ResultEnum.success}


jwt = container.jwt()

@jwt.invalid_token_loader
def custom_expired_token_callback(_):
    return {'status': ResultEnum.error.value}, 422

