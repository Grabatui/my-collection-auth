from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

from app.core.persistence.repository import Database, UserRepository
from app.core.useCase.registration import RegisterUseCase
from app.core.useCase.auth import AuthorizeWithCredentialsUseCase
from app.core.domain.common import SourceTokensProvider
from app.core.domain.registration import PasswordValidator, UserFactory
from app.core.persistence.action.common import ConvertSourceTokenAction, EncodePasswordAction
from app.core.persistence.action.registration import CreateUserAction, IsUsernameAlreadyExistsAction
from app.core.persistence.action.auth import AreAuthorizeCredentialsCorrectAction, GenerateAccessAndRefreshTokensAction
from app.core.persistence.model.registration import NewUserModel


class Container(containers.DeclarativeContainer):
    configuration = providers.Configuration()

    app = flask.Application(Flask, __name__)
    apiV1 = flask.Extension(Api)
    jwt = flask.Extension(JWTManager)


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
    areAuthorizeCredentialsCorrect = providers.Factory(
        AreAuthorizeCredentialsCorrectAction,
        userRepository=userRepository
    )
    generateAccessAndRefreshTokens = providers.Factory(
        GenerateAccessAndRefreshTokensAction,
        jwtExpiresIn=configuration.jwt_expires_seconds
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
    athorizeWithCredentialsUseCase = providers.Factory(
        AuthorizeWithCredentialsUseCase,
        encodePassword=encodePassword,
        areAuthorizeCredentialsCorrect=areAuthorizeCredentialsCorrect,
        generateAccessAndRefreshTokens=generateAccessAndRefreshTokens
    )
