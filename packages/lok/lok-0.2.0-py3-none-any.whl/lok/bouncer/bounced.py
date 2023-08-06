from ..enums import LokGrantType
from ..token import JwtToken
import logging
from django.contrib.sessions.backends.db import SessionStore
import asyncio

class BounceException(Exception):
    pass

logger = logging.getLogger(__name__)



class Bounced:

    def __init__(self, user, client, scopes, token=None, is_jwt=False) -> None:
        self._user = user
        self._client = client
        self._scopes = scopes or []
        self.scopeset = set(self._scopes)
        self.is_jwt = is_jwt
        self.token = token

    @property
    def user(self):
        return self._user

    @property
    def client(self):
        return self._client

    @property
    def app(self):
        return self._client.app

    @property
    def scopes(self):
        return self._scopes

    @property
    def roles(self):
        return self.user.roles


    def bounce(self, required_roles=[], required_scopes=[], anonymous=False, only_jwt=False):

        required_scopes = set(required_scopes)
        required_roles = set(required_roles)

        if only_jwt and not self.is_jwt:
            raise BounceException("Only Apps authorized via JWT are allowed here")
       
        if self._client.grant_type == LokGrantType.CLIENT_CREDENTIALS.value:
            if not required_scopes.issubset(self.scopeset):
                raise BounceException(f"App has not the required Scopes. Required {required_scopes}")

        if self._client.grant_type == LokGrantType.IMPLICIT.value:
            if not anonymous and self.user.is_anonymous:
                raise BounceException("Only signed in users are allowed here")
    
        # Scope tests
        if self._client.grant_type == LokGrantType.PASSWORD.value:
            return True


    @classmethod
    def from_auth(cls, auth: JwtToken):
        return cls(auth.user, auth.app, auth.scopes, token=auth.token, is_jwt=True)
