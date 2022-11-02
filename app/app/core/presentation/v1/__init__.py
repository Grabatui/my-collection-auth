from app.main import container, app


api = container.apiV1()
api.prefix = '/v1'


from . import registration, auth, check


container.wire(modules=[registration, auth, check])

api.add_resource(registration.Register, '/register')
api.add_resource(auth.Login, '/login')
api.add_resource(auth.RefreshToken, '/refresh')
api.add_resource(check.Check, '/check')

api.init_app(app)

jwt = container.jwt()
jwt.init_app(app)
