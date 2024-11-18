import jwt
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


@database_sync_to_async
def get_user_from_jwt(token):
    try:
        # Decode the JWT token
        decoded_data = UntypedToken(token)
        user_model = get_user_model()
        user_id = decoded_data['user_id']
        user = user_model.objects.get(id=user_id)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, user_model.DoesNotExist):
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token = headers.get(b'authorization', None)

        if token is not None:
            try:
                # Extract the token after "Bearer"
                token = token.decode().split(" ")[1]
                print("Token:", token)
                scope['user'] = await get_user_from_jwt(token)
            except Exception as e:
                print("Error in token validation:", e) 
                scope['user'] = AnonymousUser()
        else:
            print("No authorization header found.")
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
