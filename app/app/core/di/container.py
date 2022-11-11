from dependency_injector import containers, providers
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

from app.core.persistence.repository import Database, UserRepository
from app.core.useCase.registration import RegisterUseCase
from app.core.useCase.auth import AuthorizeWithCredentialsUseCase, RefreshTokenUseCase
from app.core.domain.common import SourceTokensProvider, LoggerProvider
from app.core.domain.auth import AuthorizedIdentityProvider
from app.core.domain.registration import PasswordValidator, UserFactory
from app.core.persistence.action.common import ConvertSourceTokenAction, EncodePasswordAction
from app.core.persistence.action.registration import CreateUserAction, IsUsernameAlreadyExistsAction
from app.core.persistence.action.auth import AreAuthorizeCredentialsCorrectAction, GenerateAccessAndRefreshTokensAction
from app.core.persistence.model.registration import NewUserModel


class Container(containers.DeclarativeContainer):
    configuration = providers.Configuration()

    app = providers.Singleton(Flask, __name__)
    apiV1 = providers.Singleton(Api)
    jwt = providers.Singleton(JWTManager)


    database = providers.Singleton(
        Database,
        database_string=configuration.database_string
    )
    userRepository = providers.Singleton(
        UserRepository,
        database=database
    )


    newUserModel = providers.Singleton(NewUserModel)


    convertSourceToken = providers.Singleton(ConvertSourceTokenAction)
    encodePassword = providers.Singleton(
        EncodePasswordAction,
        salt=configuration.password_salt
    )
    createUser = providers.Singleton(
        CreateUserAction,
        userRepository=userRepository,
        newUserModel=newUserModel
    )
    isUsernameAlreadyExists = providers.Singleton(
        IsUsernameAlreadyExistsAction,
        userRepository=userRepository
    )
    areAuthorizeCredentialsCorrect = providers.Singleton(
        AreAuthorizeCredentialsCorrectAction,
        userRepository=userRepository
    )
    generateAccessAndRefreshTokens = providers.Singleton(
        GenerateAccessAndRefreshTokensAction,
        jwtAccessTokenExpiresIn=configuration.jwt_access_token_expires_seconds,
        jwtRefreshTokenExpiresIn=configuration.jwt_refresh_token_expires_seconds
    )


    sourceTokensProvider = providers.Singleton(
        SourceTokensProvider,
        tokensBySources=configuration.tokens_by_sources,
        convertSourceToken=convertSourceToken
    )
    userFactory = providers.Singleton(
        UserFactory,
        encodePassword=encodePassword
    )
    passwordValidator = providers.Singleton(PasswordValidator)
    authorizedIdentityProvider = providers.Singleton(AuthorizedIdentityProvider)
    loggerProvider = providers.Singleton(
        LoggerProvider,
        logRootPath=configuration.root_path
    )


    registerUseCase = providers.Singleton(
        RegisterUseCase,
        userFactory=userFactory,
        createUser=createUser
    )
    athorizeWithCredentialsUseCase = providers.Singleton(
        AuthorizeWithCredentialsUseCase,
        encodePassword=encodePassword,
        areAuthorizeCredentialsCorrect=areAuthorizeCredentialsCorrect,
        generateAccessAndRefreshTokens=generateAccessAndRefreshTokens
    )
    refreshTokenUseCase = providers.Singleton(
        RefreshTokenUseCase,
        authorizedIdentityProvider=authorizedIdentityProvider,
        generateAccessAndRefreshTokens=generateAccessAndRefreshTokens
    )
