from django.urls import path
from .views import FileDeleteView, UserRegisterView, UserLoginView, UserLogoutView, FileListView, FileUploadView, FileDownloadView


urlpatterns = [
    # authentication
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/<str:username>/', UserLogoutView.as_view(), name='user_logout'),

    # files operation
    path('file/', FileListView.as_view(), name='file_list'),
    path('file/upload/', FileUploadView.as_view(), name='file_upload'),
    path('file/download/<int:pk>/', FileDownloadView.as_view(), name='file_download'),
    path('file/delete/<int:pk>/', FileDeleteView.as_view(), name='file_delete'),
         
    ]