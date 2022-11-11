from enum import Enum
from typing import Optional
from flask_restx import Resource, fields
from flask_restx.fields import Raw
from dependency_injector.wiring import Provide
from flask import request

from app.core.domain.common import SourceTokensProvider, LoggerProvider
from app.core.di.container import Container


marshal_error_fields = {
    'error': fields.String,
    'fields': fields.Raw
}


class ResultEnum(Enum):
    success = 'success'
    error = 'error'


class ResultField(Raw):
    def format(self, value):
        return value.value if isinstance(value, ResultEnum) else ResultEnum.error.value


class AbstractResource(Resource):
    def __init__(
        self,
        api=None,
        loggerProvider: LoggerProvider = Provide[Container.loggerProvider],
        *args,
        **kwargs
    ):
        self.__loggerProvider = loggerProvider

        super().__init__(api, *args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        methodFullName = self.__class__.__name__ + '.' + request.method.lower()
        
        data = None
        try:
            data = request.get_json()
        except Exception:
            pass

        self.__loggerProvider.get(methodFullName).addInfo(
            message='Internal Request ' + methodFullName,
            data={
                'query': request.query_string,
                'data': data,
            }
        )

        try:
            response = super().dispatch_request(*args, **kwargs)
        except Exception as exception:
            self.__loggerProvider.get(methodFullName).addInfo(
                message='Internal Exception ' + methodFullName,
                data={'error': str(exception)}
            )

            raise exception

        self.__loggerProvider.get(methodFullName).addInfo(
            message='Internal Response ' + methodFullName,
            data={'data': response}
        )

        return response

    def _send_error(
        self,
        message: str,
        additionalData: Optional[dict] = None,
        status: int = 500
    ) -> tuple:
        data = additionalData if additionalData is not None else {}

        data['error'] = message

        return {
            'status': ResultEnum.error,
            'data': data
        }, status

    def _send_form_error(
        self,
        errors: dict,
        status: int = 500
    ) -> tuple:
        return self._send_error(
            'Form is invalid',
            additionalData={'fields': errors},
            status=status
        )


def get_source_from_request_headers(
    headers,
    sourceTokensProvider: SourceTokensProvider
) -> str:
    token = None
    if 'Authorization' in headers:
        token = headers['Authorization'].split(' ')[1]

    if not token:
        raise Exception('Authentication Token is missing')

    source = sourceTokensProvider.get(token)

    if not source:
        raise Exception('Token in invalid')

    return source
