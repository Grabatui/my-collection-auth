from flask_jwt_extended import jwt_required
from flask_restx import marshal_with

from app.main import app
from app.core.presentation.v1.helpers import AbstractResource, ResultEnum, ResultField


class Check(AbstractResource):
    resource_fields = {
        'status': ResultField
    }

    @jwt_required()
    @marshal_with(fields=resource_fields, skip_none=True)
    def post(self):
        return {'status': ResultEnum.success}


jwt = app.container.jwt()

@jwt.invalid_token_loader
def custom_invalid_token_callback(_):
    return {
        'status': ResultEnum.error.value,
        'data': {'error': 'Token is invalid'}
    }, 401


@jwt.expired_token_loader
def custom_expired_token_callback(_, __):
    return {
        'status': ResultEnum.error.value,
        'data': {'error': 'Token has been expired'}
    }, 401
