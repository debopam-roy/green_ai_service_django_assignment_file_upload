from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import FileUpload
User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user_name', 'email', 'is_active', 'is_staff')
    search_fields = ('user_name', 'email', 'full_name')  
    ordering = ('full_name', 'user_name')  

admin.site.register(User, CustomUserAdmin)

class FilesUploaded(admin.ModelAdmin):
    list_display = ('id', 'file', 'user', 'file_type', 'file_size', 'uploaded_at')
    search_fields = ('file', 'file_type')  
    ordering = ('file', 'file_type')  

admin.site.register(FileUpload, FilesUploaded)