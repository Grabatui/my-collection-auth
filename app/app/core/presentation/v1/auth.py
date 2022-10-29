from flask_restful import Resource, marshal_with, reqparse, fields
from dependency_injector.wiring import Provide, inject

from app.core.di.container import Container


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)


resource_fields = {
    'access_token': fields.String,
    'refresh_token': fields.String
}


class Login(Resource):
    @inject
    @marshal_with(fields=resource_fields)
    #def post(self, searchUseCase: SearchUseCase = Provide[Container.searchUseCase]):
    def post(self):
        arguments = parser.parse_args()

        # TODO: Add unique access tokens for several projects - only they would login
        # TODO: Make here access and refresh tokens - https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
        # TODO: Create route for validation
        return {
            'access_token': 'access',
            'refresh_token': 'refresh'
        }