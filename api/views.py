from django.shortcuts import render
from api.serializers import FileSerializer, LinkSerializer
from files.models import File, Link, MyUser
from rest_framework import generics
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.parsers import JSONParser, MultiPartParser
from django.core.signing import BadSignature, SignatureExpired

# Create your views here.

class UploadLinkView(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.AllowAny,]
    parser_classes = [JSONParser]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        name = request.data['name']
        link = request.data['link']
        try:
            user = User.objects.get(username=username, password=password)
            user = MyUser.objects.get(user=user)
        except : 
            return Response(
                {"success":False, "result":None, "errors":["Invalid user credentials."]},
                status = status.HTTP_401_UNAUTHORIZED
            )
        
        link_password = get_random_string(10)
        link_data = Link(user = user, name=name, link=link, password=link_password)
        link_data.save()
        unique_link = link_data.get_absolute_url()
        return Response(
            {"success":True, "result":{"unique_link":unique_link, "password":link_password}, "errors":[]}, 
            status=status.HTTP_201_CREATED
            )


class UploadFileView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.AllowAny,]
    parser_classes = [MultiPartParser]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        name = request.data['name']
        file = request.FILES['file']
        try:
            user = User.objects.get(username=username, password=password)
            user = MyUser.objects.get(user=user)
        except : 
            return Response(
                {"success":False, "result":None, "errors":["Invalid user credentials."]},
                status = status.HTTP_401_UNAUTHORIZED
            )
        
        file_password = get_random_string(10)
        file_data = File(user = user, name=name, file=file, password=file_password)
        file_data.save()
        unique_link = file_data.get_absolute_url()
        print(unique_link)
        return Response(
            {"success":True, "result":{"unique_link":unique_link, "password":file_password}, "errors":[]}, 
            status=status.HTTP_201_CREATED
            )

class SecureLinkView(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.AllowAny,]
    parser_classes = [JSONParser]

    def post(self, request):
        password = request.data['password']
        secure_token = request.data['token']
        try:
            pk = Link.security.unsign(secure_token, max_age=86400)
            link_obj = Link.objects.get(pk=pk)
        except(BadSignature, SignatureExpired, Link.DoesNotExist):
            return Response(
                {"success":False, "result":None, "errors":["Invalid or Expired Link"]},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            link_obj = Link.objects.get(password=password)
            link_obj.no_of_correct_attempts += 1
            link_obj.save()
        except Link.DoesNotExist:
            return Response(
                {"success":False, "result":None, "errors":["Invalid or Expired Link"]},
                status = status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"success":True, "result":{"link":link_obj.link}, "errors":[]}, 
            status=status.HTTP_200_OK
            )   


class SecureFileView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.AllowAny,]
    parser_classes = [JSONParser]

    def post(self, request):
        password = request.data['password']
        secure_token = request.data['token']
        try:
            pk = File.security.unsign(secure_token, max_age=86400)
            print(pk)
            file_obj = File.objects.get(pk=pk)
        except(BadSignature, SignatureExpired, File.DoesNotExist):
            print("file insecure")
            return Response(
                {"success":False, "result":None, "errors":["Invalid or Expired Link"]},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            file_obj = File.objects.get(password=password)
            file_obj.no_of_correct_attempts += 1
            file_obj.save()
        except File.DoesNotExist:
            return Response(
                {"success":False, "result":None, "errors":["Invalid or Expired Link"]},
                status = status.HTTP_400_BAD_REQUEST
            )
        data = FileSerializer(file_obj)
        return Response(
            {"success":True, "result":data.data, "errors":[]}, 
            status=status.HTTP_200_OK,
            content_type='application/octet-stream'
            )   

