from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'full_name', 'is_active', 'is_staff')
    search_fields = ('user_name', 'email', 'full_name')  # Search functionality
    ordering = ('full_name', 'user_name',)  # Default ordering

admin.site.register(User, CustomUserAdmin)