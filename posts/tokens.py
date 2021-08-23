from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from config.settings import SIMPLE_JWT
import jwt
def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
    'access': str(refresh.access_token),
    'refresh': str(refresh)
    }

def decode_token(request):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    user , token = response
    payload = jwt.decode(str(token),SIMPLE_JWT['SIGNING_KEY'],SIMPLE_JWT['ALGORITHM'])
    return payload
