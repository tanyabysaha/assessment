from datetime import datetime, timezone


def track_last_request_middleware(get_response):
    """Tracking time of the last request user made to system"""

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        if request.user.is_authenticated:
            request.user.last_request = datetime.now(timezone.utc)
            request.user.save()

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
