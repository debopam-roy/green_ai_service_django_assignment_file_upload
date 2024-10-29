from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import File
User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'username', 'email', 'is_active', 'is_staff', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'fullname')  
    ordering = ('fullname', 'username')  

admin.site.register(User, UserAdmin)

class FileListAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'file_name', 'file_type', 'file_size')
    search_fields = ('file',)

admin.site.register(File, FileListAdmin)