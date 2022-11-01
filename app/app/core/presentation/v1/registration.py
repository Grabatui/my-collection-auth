from flask import request
from flask_restx import marshal_with, fields
from dependency_injector.wiring import Provide, inject
from wtforms import Form as BaseForm, fields as forms_fields, validators

from app.core.di.container import Container
from app.core.presentation.v1.helpers import AbstractResource, ResultEnum, ResultField, get_source_from_request_headers, marshal_error_fields
from app.core.useCase.registration import RegisterUseCase
from app.core.domain.common import SourceTokensProvider
from app.core.domain.registration import IsUsernameAlreadyExistsInterface, PasswordValidator


class Form(BaseForm):
    username = forms_fields.StringField('Username', [validators.DataRequired(), validators.Length(min=3)])
    password = forms_fields.StringField('Password', [validators.DataRequired()])

    @inject
    def validate_username(
        form,
        field: forms_fields.StringField,
        isUsernameAlreadyExists: IsUsernameAlreadyExistsInterface = Provide[Container.isUsernameAlreadyExists]
    ):
        if isUsernameAlreadyExists.run(field.data):
            raise validators.ValidationError('Username already exists')

    @inject
    def validate_password(
        form,
        field: forms_fields.StringField,
        passwordValidator: PasswordValidator = Provide[Container.passwordValidator]
    ):
        isValid, validationErrors = passwordValidator.run(field.data)

        if not isValid:
            raise validators.ValidationError(', '.join(validationErrors))


class Register(AbstractResource):
    resource_fields = {
        'status': ResultField,
        'data': fields.Nested(
            marshal_error_fields,
            allow_null=True
        )
    }

    @inject
    @marshal_with(fields=resource_fields, skip_none=True)
    def post(
        self,
        registerUseCase: RegisterUseCase = Provide[Container.registerUseCase],
        sourceTokensProvider: SourceTokensProvider = Provide[Container.sourceTokensProvider]
    ):
        try:
            source = get_source_from_request_headers(request.headers, sourceTokensProvider)
        except Exception as exception:
            return self._send_form_error(str(exception), status=401)

        form = Form(data=request.get_json())
        if not form.validate():
            return self._send_form_error(form.errors, status=400)

        if not registerUseCase.run(source, form.username.data, form.password.data):
            return {'status': ResultEnum.error}

        return {'status': ResultEnum.success}