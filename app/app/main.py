import os

from .core.di.container import Container


def create_app():
    container = Container()
    container.configuration.database_string.from_value(
        'postgresql+pg8000://{user}:{password}@{host}/{database}'.format(
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            database=os.environ['DB_DATABASE']
        )
    )
    container.configuration.tokens_by_sources.from_dict({
        'main': os.environ['SOURCE_TOKEN_MAIN'],
    })
    container.configuration.password_salt.from_env('PASSWORD_SALT')
    container.configuration.secret_key.from_env('SECRET_KEY')
    container.configuration.jwt_access_token_expires_seconds.from_env('JWT_ACCESS_TOKEN_EXPIRES_SECONDS', as_=int)
    container.configuration.jwt_refresh_token_expires_seconds.from_env('JWT_REFRESH_TOKEN_EXPIRES_SECONDS', as_=int)

    app = container.app()
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['ERROR_INCLUDE_MESSAGE'] = False

    container.configuration.root_path.from_value(
        os.path.dirname(app.instance_path)
    )

    app.container = container

    return app

def init_routes():
    from .core.presentation import v1

app = create_app()
init_routes()
