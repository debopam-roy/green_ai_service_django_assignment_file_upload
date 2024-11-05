import os
import random
import string
from django.http import Http404
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate

from filezup_backend import settings
from .models import File
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[EmailValidator(message=_("Enter a valid email address."))]
    )

    is_staff = serializers.BooleanField(default=False, required=False)
    is_active = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'password', 'is_staff', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_fullname(self, value):
        
        min_length = 3
        max_length = 100
        if not (min_length <= len(value) <= max_length):
            raise serializers.ValidationError(
                _(f"Fullname must be between {min_length} and {max_length} characters.")
            )
        return value

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("This email is already in use."))
        return value

    def validate_username(self, value):

        min_length = 3
        max_length = 50
        if not (min_length <= len(value) <= max_length):
            raise serializers.ValidationError(
                _(f"Username must be between {min_length} and {max_length} characters.")
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("This username is already in use."))
        return value

    def validate_password(self, value):

        min_length = 8
        max_length = 22
        if not (min_length <= len(value) <= max_length):
            raise serializers.ValidationError(
                _(f"Password must be between {min_length} and {max_length} characters.")
            )
        
        validate_password(value)
        return value

    def create(self, validated_data):

        user = User(
            fullname=validated_data['fullname'],
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=validated_data.get('is_staff', False),  
            is_active=validated_data.get('is_active', True),  
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=3, max_length=50)
    password = serializers.CharField(required=True, write_only=True,  min_length=8, max_length=22, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        
        user = authenticate(username=username, password=password)

        
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        
        if not user.is_active:
            raise serializers.ValidationError("This user account is inactive.")

        return {'user': user}

class UserLogoutSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    
    def validate_username(self, value):
        user = User.objects.filter(username=value).first()
        
        if not user:
            raise serializers.ValidationError("User does not exist.")
        
        self.user = user
        return value
    
    def logout_user(self):
        tokens = OutstandingToken.objects.filter(user=self.user)
        
        if not tokens.exists():
            raise serializers.ValidationError("User is already logged out.")
        
        for token in tokens:
            BlacklistedToken.objects.create(token=token)
            token.delete() 

class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'owner', 'file_name', 'file_size', 'file_type', 'uploaded_at']
 
class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'file_size', 'file_type']

    def generate_random_string(self, length=5):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def validate_file_name(self, value):
        original_name = value.name
        while File.objects.filter(file_name=value.name).exists():
            random_suffix = self.generate_random_string()
            base_name, ext = original_name.rsplit('.', 1) if '.' in original_name else (original_name, '')
            value.name = f"{base_name}_{random_suffix}.{ext}"
        return value

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user  
        file = validated_data.get('file_name')  
        validated_data['file_size'] = file.size
        validated_data['file_type'] = file.content_type
        return File.objects.create(**validated_data)

class FileDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [] 

    def validate(self, value):
        file_instance = self.instance
        if not file_instance or not file_instance.file_name:
            raise Http404("File not found or you do not have permission to delete this file.")
        return value

class FileDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'file_type']

    def validate_and_get_file_path(self, pk, user):
        try:
            file_instance = File.objects.get(pk=pk, owner=user)
        except File.DoesNotExist:
            raise Http404("File not found")
        
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_instance.file_name.name.split('/')[-1])
        if not os.path.exists(file_path):
            raise Http404("File not found")
        
        return file_path, file_instance.file_type

        