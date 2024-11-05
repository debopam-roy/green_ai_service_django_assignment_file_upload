import os
from django.http import FileResponse, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer, FileListSerializer, FileUploadSerializer, FileDeleteSerializer, FileDownloadSerializer
from rest_framework.parsers import MultiPartParser, FormParser 
from .models import File


def getUserDetails(message, user, status):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    response = Response({
        "message": message,
        "user_id": user.id,
        "username": user.username,
        "fullname": user.fullname,
        "email": user.email,
        "access_token": str(access_token),
        "refresh_token": str(refresh_token)
    }, status=status)

    response.set_cookie(
        key='access_token',
        value=str(access_token),  
        httponly=True,
        samesite='Lax',
        secure=True  
    )  
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),  
        httponly=True,
        samesite='Lax',
        secure=True  
    )
    
    return response


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class UserLoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)   
        serializer.is_valid(raise_exception=True)     
        user = serializer.validated_data['user'] 

        return getUserDetails("User logged in successfully", user, status.HTTP_200_OK)

class UserLogoutView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data={'username': kwargs['username']})
        serializer.is_valid(raise_exception=True)
        serializer.logout_user()
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

class FileListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileListSerializer

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

class FileUploadView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileUploadSerializer

    def create(self, request, *args, **kwargs):
        uploaded_files = request.FILES.getlist('file')
        responses = []
        
        for uploaded_file in uploaded_files:
            serializer = self.get_serializer(data={
                'file_name': uploaded_file,
                'owner': request.user
            })
            
            if serializer.is_valid():
                file_upload_instance = serializer.save()
                responses.append({
                    'filename': file_upload_instance.file_name.name,
                    'status': 'uploaded successfully',
                    'uploaded_at': file_upload_instance.uploaded_at
                })
            else:
                responses.append({
                    'filename': uploaded_file.name,
                    'status': 'upload failed',
                    'errors': serializer.errors
                })
        message = 'Files upload complete' if len(uploaded_file) > 1 else 'File upload complete'
        return Response({
            'data': responses,
            'status': {
                'code': status.HTTP_201_CREATED,
                'message': message
            }
        }, status=status.HTTP_201_CREATED)

class FileDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileDeleteSerializer

    def delete(self, request, pk):
        try:
            file_instance = File.objects.get(pk=pk, owner = request.user)
            if file_instance.file_name and os.path.exists(file_instance.file_name.path):
                os.remove(file_instance.file_name.path) 
                file_instance.delete()
                return Response({"message": "Deletion successful"}, status=status.HTTP_200_OK)
            return Response({"message": "File not found."}, status=status.HTTP_204_NO_CONTENT)
 
        except File.DoesNotExist:
            raise Http404("File not found or you do not have permission to delete this file.")
          
class FileDownloadView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileDownloadSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        
        file_path, file_type = serializer.validate_and_get_file_path(kwargs['pk'], request.user)

        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Type'] = file_type
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response

