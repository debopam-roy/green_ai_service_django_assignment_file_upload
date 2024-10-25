from .models import FileUpload
from rest_framework.views import APIView
from rest_framework import status,generics
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.parsers import MultiPartParser, FormParser 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer, FileUploadSerializer


User = get_user_model()


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = RefreshToken.for_user(user)

            response_data = {
                'data': {
                    'user_name': user.user_name,
                    'access_token': str(token.access_token),
                },
                'status': {
                    'code': status.HTTP_201_CREATED,
                    'message': 'User registration successful',
                }
            }

            response = Response(response_data, status=status.HTTP_201_CREATED)

            # Store the access and refresh tokens in HttpOnly, Secure cookies
            response.set_cookie(
                key='access_token',
                value=str(token.access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=60 * 60 * 24,  # 1 day expiry for access token
            )
            response.set_cookie(
                key='refresh_token',
                value=str(token),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=60 * 60 * 24 * 7  # 7 days expiry for refresh token
            )

            response['Authorization'] = f'Bearer {str(token.access_token)}'
            response['Refresh-Token'] = str(token)
            return response

        except ValidationError as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User registration unsuccessful',
                    'errors': e.message_dict,
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
            # Validate login data
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token = RefreshToken.for_user(user)

            response_data = {
                'data': {
                    'user_name': user.user_name,
                    'access_token': str(token.access_token),
                },
                'status': {
                    'code': status.HTTP_200_OK,
                    'message': 'User login successful',
                }
            }

            response = Response(response_data, status=status.HTTP_200_OK)

            # Store the access and refresh tokens in HttpOnly, Secure cookies
            response.set_cookie(
                key='access_token',
                value=str(token.access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=60 * 60 * 24,  # 1 day expiry for access token
            )
            response.set_cookie(
                key='refresh_token',
                value=str(token),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=60 * 60 * 24 * 7  # 7 days expiry for refresh token
            )

            response['Authorization'] = f'Bearer {str(token.access_token)}'
            response['Refresh-Token'] = str(token)
            return response

        except ValidationError as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User login unsuccessful',
                    'errors': e.message_dict,
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
            # Validate input data
            serializer = UserLogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_name = serializer.validated_data['user_name']

            try:
                user = User.objects.get(user_name=user_name)
            except User.DoesNotExist:
                return Response({
                    'data': {},
                    'status': {
                        'code': status.HTTP_404_NOT_FOUND,
                        'message': 'User not found.',
                    }
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                refresh_token = RefreshToken.for_user(user)
                refresh_token.blacklist()
            except Exception as e:
                return Response({
                    'data': {},
                    'status': {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': 'Failed to blacklist the token.',
                        'error': str(e),
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = Response({
                'data': {},
                'status': {
                    'code': status.HTTP_200_OK,
                    'message': 'User logout successful.'
                }
            }, status=status.HTTP_200_OK)

            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except ValidationError as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid data provided for logout.',
                    'errors': e.message_dict,
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'An unexpected error occurred during logout.',
                    'error': str(e),
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
        
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Authentication credentials were not provided.'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
        jwt_authentication = JWTAuthentication()

        try:
            validated_token = jwt_authentication.get_validated_token(access_token)
            user = jwt_authentication.get_user(validated_token)
        except TokenError as e:
            return Response({
                'data': {},
                'status': {
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'message': str(e),
                }
            }, status=status.HTTP_401_UNAUTHORIZED)

        uploaded_files = request.FILES.getlist('file')
        responses = []

        for uploaded_file in uploaded_files:
            serializer = FileUploadSerializer(data={
                'file': uploaded_file,
                'user': user.id, 
            })

            if serializer.is_valid(): 
                file_upload_instance = serializer.save() 
                responses.append({
                    'filename': file_upload_instance.file.name,
                    'status': 'uploaded successfully',
                    'uploaded_at': file_upload_instance.uploaded_at
                })
            else:
                responses.append({
                    'filename': uploaded_file.name,
                    'status': 'upload failed',
                    'errors': serializer.errors
                })

        return Response({
            'data': responses,
            'status': {
                'code': status.HTTP_201_CREATED,
                'message': 'File(s) upload attempt complete'
            }
        }, status=status.HTTP_201_CREATED)


class FileUploadListView(generics.ListAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FileUpload.objects.filter(user=self.request.user)


class FileDownloadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        try:
            file_instance = FileUpload.objects.get(pk=pk, user=request.user)
            response = FileResponse(file_instance.file.open('rb'), as_attachment=True)
            return response
        except FileUpload.DoesNotExist:
            raise Http404


class FileDeleteView(generics.DestroyAPIView):
    queryset = FileUpload.objects.all()
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, *args, **kwargs):
        try:
            file_instance = FileUpload.objects.get(pk=pk, user=request.user)
            file_instance.delete()
            return Response({"message": "File deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FileUpload.DoesNotExist:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

