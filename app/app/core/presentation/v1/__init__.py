from flask_log_request_id import RequestID

from app.main import app


api = app.container.apiV1()
api.prefix = '/v1'


from . import registration, auth, check


app.container.wire(modules=[registration, auth, check])

api.add_resource(registration.Register, '/register')
api.add_resource(auth.Login, '/login')
api.add_resource(auth.RefreshToken, '/refresh')
api.add_resource(check.Check, '/check')

api.init_app(app)

jwt = app.container.jwt()
jwt.init_app(app)

RequestID(app)
