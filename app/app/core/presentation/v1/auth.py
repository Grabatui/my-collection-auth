from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import marshal_with, reqparse, fields
from dependency_injector.wiring import Provide, inject
from wtforms import Form as BaseForm, fields as forms_fields, validators

from app.core.di.container import Container
from app.core.presentation.v1.helpers import AbstractResource, ResultEnum, ResultField, get_source_from_request_headers, marshal_error_fields
from app.core.domain.common import SourceTokensProvider
from app.core.useCase.auth import AuthorizeWithCredentialsUseCase, RefreshTokenUseCase


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)


class Form(BaseForm):
    username = forms_fields.StringField('Username', [validators.DataRequired(), validators.Length(min=3)])
    password = forms_fields.StringField('Password', [validators.DataRequired()])


data = marshal_error_fields.copy()
data.update({
    'access_token': fields.String,
    'refresh_token': fields.String,
    'expires_in': fields.Integer
})
resource_fields = {
    'status': ResultField,
    'data': fields.Nested(
        data,
        allow_null=True,
        skip_none=True
    )
}


class Login(AbstractResource):
    @inject
    @marshal_with(fields=resource_fields, skip_none=True)
    def post(
        self,
        sourceTokensProvider: SourceTokensProvider = Provide[Container.sourceTokensProvider],
        authorizeWithCredentialsUseCase: AuthorizeWithCredentialsUseCase = Provide[Container.athorizeWithCredentialsUseCase]
    ):
        try:
            get_source_from_request_headers(request.headers, sourceTokensProvider)
        except Exception as exception:
            return self._send_form_error(str(exception), status=401)

        form = Form(data=request.get_json())
        if not form.validate():
            return self._send_form_error(form.errors, status=400)

        try:
            tokens = authorizeWithCredentialsUseCase.run(
                username=form.username.data,
                decodedPassword=form.password.data
            )
        except Exception as exception:
            return self._send_error(str(exception), status=401)

        return {
            'status': ResultEnum.success,
            'data': {
                'access_token': tokens.accessToken,
                'refresh_token': tokens.refreshToken,
                'expires_in': tokens.expiresIn
            }
        }


class RefreshToken(AbstractResource):
    @jwt_required(refresh=True)
    @inject
    @marshal_with(fields=resource_fields, skip_none=True)
    def post(
        self,
        refreshTokenUseCase: RefreshTokenUseCase = Provide[Container.refreshTokenUseCase]
    ):
        try:
            tokens = refreshTokenUseCase.run()
        except Exception as exception:
            return self._send_error(str(exception), status=401)

        return {
            'status': ResultEnum.success,
            'data': {
                'access_token': tokens.accessToken,
                'refresh_token': tokens.refreshToken,
                'expires_in': tokens.expiresIn
            }
        }
