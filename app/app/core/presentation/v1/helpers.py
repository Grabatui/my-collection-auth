from enum import Enum
from typing import Optional
from flask_restful import Resource, fields
from flask_restful.fields import Raw


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
