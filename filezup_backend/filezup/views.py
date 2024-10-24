from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .serializer import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # Raise exception if invalid
            user = serializer.save()

            # Generate tokens
            token = RefreshToken.for_user(user)
            response_data = {
                'data': {
                    'user_name': user.user_name,
                    'access_token': str(token.access_token),
                },
                'status': {
                    'code': status.HTTP_201_CREATED,
                    'message': 'User registration successful'
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User registration unsuccessful',
                    'errors': e.message_dict,  # Include error details
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'An unexpected error occurred',
                    'error': str(e),
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # Raise exception if invalid
            user = serializer.validated_data['user']

            # Generate tokens
            token = RefreshToken.for_user(user)
            response_data = {
                'data': {
                    'user_name': user.user_name,
                    'access_token': str(token.access_token),
                },
                'status': {
                    'code': status.HTTP_200_OK,
                    'message': 'User login successful'
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User login unsuccessful',
                    'errors': e.message_dict,  # Include error details
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'An unexpected error occurred during login',
                    'error': str(e),
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserLogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # Validate data

            user_name = serializer.validated_data['user_name']
            user = User.objects.get(user_name=user_name)

            # Deactivate user (logout)
            user.is_active = False
            user.save()

            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_200_OK,
                    'message': 'User logout successful.'
                }
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'User not found',
                }
            }, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid data provided for logout',
                    'errors': e.message_dict,  # Include error details
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'An unexpected error occurred during logout',
                    'error': str(e),
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
