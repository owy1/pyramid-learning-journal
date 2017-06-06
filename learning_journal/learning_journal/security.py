"""Security for a journal application."""
import os
from passlib.apps import custom_app_context as pwd_context
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated
from pyramid.security import Allow


class MyRoot(object):
    """Override root class for security."""

    def __init__(self, request):
        """Override root for security.py."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'secret')
    ]


def check_credentials(username, password):
    """Validate credentials."""
    stored_username = os.environ.get('AUTH_USERNAME')
    stored_password = os.environ.get('AUTH_PASSWORD')
    is_authenticated = False
    if stored_username and stored_password:
        if username == stored_username:
                is_authenticated = pwd_context.verify(password, stored_password)
    return is_authenticated


def includeme(config):
    """Security-related configuration."""
    auth_secret = os.environ.get('AUTH_SECRET')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(MyRoot)
