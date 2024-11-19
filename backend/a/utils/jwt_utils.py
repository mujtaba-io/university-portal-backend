import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone
from ..models import User


def create_jwt_token(username):
    expiration = datetime.now(timezone.utc) + settings.JWT_EXPIRATION_DELTA
    token = jwt.encode(
        {
            "username": username,
            "exp": expiration,
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None







# Defining the @token_required decorator
# -- so any function will be sure that the user is authenticated
from django.http import JsonResponse

def token_required(func):
  """
  Decorator to validate JWT token before executing the view function.
  """
  def wrapper(request, *args, **kwargs):
    token = request.headers.get('token')

    if not token:
      return JsonResponse({"error": "Token is required"}, status=401)

    username = decode_jwt_token(token)  # Replace with your JWT decoding function

    if not username:
      return JsonResponse({"error": "Invalid token"}, status=401)

    print(f"Authenticated user: {username}")
    request.user = User.objects.get(username=username)  # Attach user object to request
    return func(request, *args, **kwargs)
  return wrapper