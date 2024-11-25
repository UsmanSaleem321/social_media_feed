from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from asgiref.sync import sync_to_async

User = get_user_model()

class CustomAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get session key from cookies
        session_key = scope['cookies'].get('sessionid')
        
        # Retrieve user associated with session key
        if session_key:
            try:
                session = await sync_to_async(Session.objects.get)(session_key=session_key)
                user_id = session.get_decoded().get('_auth_user_id')
                scope['user'] = await sync_to_async(User.objects.get)(id=user_id)
            except (Session.DoesNotExist, User.DoesNotExist):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
