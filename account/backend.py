from django.contrib.auth.backends import ModelBackend
from .models import User


class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(mobile_number=username)
            if user.check_password(password):
                return user
            
        
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
            

        if user.check_password(password):
            return user
        
        return None