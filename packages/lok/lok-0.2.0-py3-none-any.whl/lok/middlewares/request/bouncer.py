import asyncio
from asgiref.sync import sync_to_async
from django.utils.decorators import sync_and_async_middleware
from ...bouncer.bounced import Bounced




@sync_and_async_middleware
def BouncedMiddleware(get_response):
    # One-time configuration and initialization goes here.
    if asyncio.iscoroutinefunction(get_response):
        async def middleware(request):
            # Do something here!
            if hasattr(request, "auth"):
                bounced = Bounced.from_auth(request.auth)
                setattr(request, "bounced", bounced)
                setattr(request, "user", bounced.user)
                setattr(request, "app", bounced.app)
                setattr(request, "client", bounced.client)
            response = await get_response(request)
            return response

    else:
        def middleware(request):
            # Do something here!
            if hasattr(request, "auth"):
                bounced = Bounced.from_auth(request.auth)
                setattr(request, "bounced", bounced)
                setattr(request, "user", bounced.user)
                setattr(request, "app", bounced.app)
                setattr(request, "client", bounced.client)
            response = get_response(request)
            return response

    return middleware