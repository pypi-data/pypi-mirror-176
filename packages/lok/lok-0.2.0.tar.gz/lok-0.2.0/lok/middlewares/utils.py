from ..models import LokUser, LokApp, LokClient
from django.core.exceptions import  PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http.response import HttpResponseBadRequest
from asgiref.sync import async_to_sync, sync_to_async
from ..token import JwtToken
from django.core.exceptions import ObjectDoesNotExist

import logging

logger = logging.getLogger(__name__)

import uuid

def decoded_to_username(decoded):
    return f"{decoded['iss']}__{decoded['sub']}"


def update_or_create_lok(decoded):
    if "sub" in decoded and decoded["sub"] is not None:
        if "iss" in decoded and decoded["iss"] is not None:
            try:
                user = get_user_model().objects.get(username=decoded_to_username(decoded))
                roles = [group.name for group in user.groups.all()]
                if "roles" in decoded and decoded["roles"] is not None:
                    if decoded["roles"] != roles:
                        user.groups.clear()
                        for role in decoded["roles"]:
                            g, _ = Group.objects.get_or_create(name=role)
                            user.groups.add(g)
                        user.save()
            except ObjectDoesNotExist:
                user = get_user_model()(sub=decoded["sub"], username=decoded_to_username(decoded), iss=decoded["iss"], first_name=decoded.get("preferred_username", None))
                user.set_unusable_password()
                user.save()
                if "roles" in decoded and decoded["roles"] is not None:
                    for role in decoded["roles"]:
                        g, _ = Group.objects.get_or_create(name=role)
                        user.groups.add(g)
                        user.save()
                logger.warning("Created new user")
    else:
        user = None

    if "client_id" in decoded and decoded["client_id"] is not None:
        try:
            client = LokClient.objects.select_related("app").get(client_id=decoded["client_id"], iss=decoded["iss"])
        except LokClient.DoesNotExist:
            if "version" in decoded:
                app, _ = LokApp.objects.get_or_create(version=decoded["version"], identifier=decoded["identifier"])
            else:
                app = None

            client = LokClient(client_id=decoded["client_id"], grant_type=decoded["type"], app=app, iss=decoded["iss"])
            client.save()
            logger.warning("Created new app")
    else:
        client = None

    return user, client


@sync_to_async
def set_request_async(request, decoded, token):
    user, app = update_or_create_lok(decoded)
    request.auth = JwtToken(decoded, user, app, token)
    request.user = user
    return request

def set_request_sync(request, decoded, token):
    user, app = update_or_create_lok(decoded)
    request.auth = JwtToken(decoded, user, app, token)
    request.user = user
    return request


@sync_to_async
def set_scope_async(scope, decoded, token):
    user, app = update_or_create_lok(decoded)
    scope["auth"] = JwtToken(decoded, user, app, token)
    scope["user"] = user
    return scope
