import os
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer, FileListSerializer, FileUploadSerializer
from rest_framework_simplejwt.tokens import RefreshToken
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
        "token": str(access_token)
    }, status=status)

    # Set cookies with access and refresh tokens
    response.set_cookie(
        key='access_token',
        value=str(access_token),  # Serialize the token
        httponly=True,
        samesite='Lax',
        secure=True  # Ensure this flag is set for production (HTTPS)
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),  # Serialize the token
        httponly=True,
        samesite='Lax',
        secure=True  # Ensure this flag is set for production (HTTPS)
    )
    
    return response

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data) 
        if serializer.is_valid():
            user = serializer.save()
            
            return getUserDetails("User registered successfully", user, status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data) 
        if serializer.is_valid():
            user = serializer.save()
            return getUserDetails( "User logged in successfully", user, status.HTTP_200_OK)        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, username):
        serializer = UserLogoutSerializer(data={'username': username})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'User logged out successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileListView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        files = File.objects.filter(owner=request.user)
        serializer = FileListSerializer(files, many=True)
        return Response(serializer.data) 

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        uploaded_files = request.FILES.getlist('file')
        responses = []

        for uploaded_file in uploaded_files:
            serializer = FileUploadSerializer(data={
                'file_name':uploaded_file,
                'owner': request.user  
            }, context={'request': request})  

            if serializer.is_valid():
                file_upload_instance = serializer.save() 
                responses.append({
                    'filename': file_upload_instance.file_name.name,  # Access the correct attribute
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

class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]  

    def delete(self, request, pk):
        try:
            file_instance = File.objects.get(pk=pk, owner = request.user)
            if file_instance.file_name and os.path.exists(file_instance.file_name.path):
                os.remove(file_instance.file_name.path) 
            file_instance.delete()
            return Response({"message": "Deletion successful"}, status=status.HTTP_204_NO_CONTENT) 
        except File.DoesNotExist:
            raise Http404("File not found or you do not have permission to delete this file.")

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            file_instance = File.objects.get(pk=pk, owner=request.user)
            response = FileResponse(file_instance.file_name.open('rb'), as_attachment=True)
            return response
        except File.DoesNotExist:
            raise Http404('File Not Found')

