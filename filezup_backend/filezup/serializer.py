from .models import FileUpload
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        max_length=22,
        min_length=8,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'user_name', 'email', 'full_name', 'password', 'is_staff', 'is_active')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  
        user.save()
        return user

    def validate_user_name(self, value):
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

class UserLoginSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('user_name', 'password')

    def validate(self, attrs):
        user_name = attrs.get('user_name')
        password = attrs.get('password')

        # Authenticate user
        user = authenticate(username=user_name, password=password)
        if user is None:
            raise serializers.ValidationError(_('Invalid username or password.'))

        user.is_active = True
        user.save()
        attrs['user'] = user  

        return attrs

class UserLogoutSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)

    def validate_user_name(self, value):
        if not User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError(_('User does not exist.'))
        return value
    
class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'uploaded_at', 'user', 'file_size', 'file_type']

    def create(self, validated_data):
        file = validated_data.get('file')
        file_size = file.size
        file_type = file.content_type  
        validated_data['file_size'] = file_size
        validated_data['file_type'] = file_type
        file_upload_instance = FileUpload.objects.create(**validated_data)

        return file_upload_instance
