import jwt
from django.http import JsonResponse
from functools import wraps
from thesis_api.settings import SECRET_KEY


def jwt_auth_needed(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        
        #token = token.split('\'')[1]

        if not token:
            return JsonResponse({'error': 'No JWT token found'})
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'JWT token has expired'})
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid JWT token'})
        
        # Set the user ID as a request attribute for the view function to use
        request.user_id = decoded_token.get('user_id')
        
        return view_func(request, *args, **kwargs)
    return wrapper


from functools import wraps
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import jwt

User = get_user_model()

def jwt_staff_auth_needed(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
       # token = token.split('\'')[1]

        if not token:
            return JsonResponse({'error': 'No JWT token found'})
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'JWT token has expired'})
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid JWT token'})
        
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token['id']
            user = User.objects.get(id=user_id.replace('-', ''))

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'})
        
        if not user.is_staff:
            return JsonResponse({'error': 'You are not authorized to perform this action'})
        
        request.user = user
        return view_func(request, *args, **kwargs)
    
    return wrapper
