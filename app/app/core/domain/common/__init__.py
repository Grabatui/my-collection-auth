from typing import Optional

from app.core.domain.entity import Logger


class EncodePasswordInterface():
    def run(self, decodedPassword: str) -> str:
        raise Exception('Method must be implemented')


class ConvertSourceTokenInterface():
    def run(self, raw_token: str) -> str:
        raise Exception('Method must be implemented')


class SourceTokensProvider():
    def __init__(
        self,
        tokensBySources: dict,
        convertSourceToken: ConvertSourceTokenInterface
    ) -> None:
        self.tokensBySources = tokensBySources
        self.convertSourceToken = convertSourceToken

    def get(self, token: str) -> Optional[str]:
        formattedToken = self.convertSourceToken.run(token)

        for source, checkToken in self.tokensBySources.items():
            if checkToken == formattedToken:
                return source

        return None


class LoggerProvider():
    def __init__(self, logRootPath: str) -> None:
        self.logRootPath = logRootPath

    def get(self, name: str) -> Logger:
        return Logger(name, self.logRootPath)
