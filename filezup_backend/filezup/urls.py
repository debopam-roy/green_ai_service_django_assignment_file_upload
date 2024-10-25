from django.urls import path
from .views import UserLoginView, UserRegisterView, UserLogoutView, FileUploadView, FileUploadListView, FileDownloadView, FileDeleteView
urlpatterns = [
    #user login routing
    path('login/', UserLoginView.as_view(), name='user_login'),
    
    #user register routing
    path('register/', UserRegisterView.as_view(), name='user_register'),
    
    #user logout routing
    path('logout/<str:user_name>/', UserLogoutView.as_view(), name='user_logout'), 

    #files upload routing
    path('files/upload/', FileUploadView.as_view(), name='file_upload'),  

    #files list routing
    path('files/', FileUploadListView.as_view(), name='file-list'),

    #files download routing
    path('files/download/<int:pk>/', FileDownloadView.as_view(), name='file-download'),

    #files delete routing
    path('files/delete/<int:pk>/', FileDeleteView.as_view(), name='file-delete'),

]