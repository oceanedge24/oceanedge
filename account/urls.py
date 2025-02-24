from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView, PasswordChangeDoneView
from .views import (
    profile, SignUpView, CustomPasswordChangeView, select_profile_icon
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('profile', profile, name="profile"),

    path('change-password/', CustomPasswordChangeView.as_view(),
         name='change_password'),
    path('password-change-done',PasswordChangeDoneView.as_view(
         template_name='registration/password__change_done.html'
            ),
         name='password_change_done'
         ),
    

    path('select-icon/', select_profile_icon, name='select_profile_icon'),
]
