from app.main import container, app


api = container.apiV1()
api.prefix = '/v1'


from . import registration
from . import auth


container.wire(modules=[registration, auth])

api.add_resource(registration.Register, '/register')
api.add_resource(auth.Login, '/login')

api.init_app(app)
