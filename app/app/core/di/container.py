from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
from flask_restful import Api

from app.core.persistence.repository import Database, UserRepository
from app.core.useCase.registration import RegisterUseCase
from app.core.domain.registration import PasswordValidator, SourceTokensProvider, UserFactory
from app.core.persistence.action.registration import ConvertSourceTokenAction, CreateUserAction, EncodePasswordAction, IsUsernameAlreadyExistsAction
from app.core.persistence.model.registration import NewUserModel


class Container(containers.DeclarativeContainer):
    app = flask.Application(Flask, __name__)
    apiV1 = flask.Extension(Api)

    configuration = providers.Configuration()


    database = providers.Factory(
        Database,
        database_string=configuration.database_string
    )
    userRepository = providers.Factory(
        UserRepository,
        database=database
    )


    newUserModel = providers.Singleton(NewUserModel)


    convertSourceToken = providers.Singleton(ConvertSourceTokenAction)
    encodePassword = providers.Factory(
        EncodePasswordAction,
        salt=configuration.password_salt
    )
    createUser = providers.Factory(
        CreateUserAction,
        userRepository=userRepository,
        newUserModel=newUserModel
    )
    isUsernameAlreadyExists = providers.Factory(
        IsUsernameAlreadyExistsAction,
        userRepository=userRepository
    )


    sourceTokensProvider = providers.Factory(
        SourceTokensProvider,
        tokensBySources=configuration.tokens_by_sources,
        convertSourceToken=convertSourceToken
    )
    userFactory = providers.Factory(
        UserFactory,
        encodePassword=encodePassword
    )
    passwordValidator = providers.Singleton(PasswordValidator)


    registerUseCase = providers.Factory(
        RegisterUseCase,
        userFactory=userFactory,
        createUser=createUser
    )
