from urllib import request

from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class  RegisterAPIView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        print(username, password, email)
        return Response({"status":"success"})

