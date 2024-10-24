from django.urls import path
from .views import UserLoginView, UserRegisterView, UserLogoutView
urlpatterns = [
    #user login routing
    path('login/', UserLoginView.as_view(), name='user_login'),
    
    #user register routing
    path('register/', UserRegisterView.as_view(), name='user_register'),
    
    #user logout routing
    path('logout/<str:user_name>/', UserLogoutView.as_view(), name='user_logout'), 
]