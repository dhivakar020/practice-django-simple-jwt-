from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .models import User
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer



@api_view(['POST'])
def register_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Create the user

        # Generate JWT token upon signup
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User created successfully!',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate the user
        user = authenticate(request, username=email, password=password)  # Email is treated as username here
        if user:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            # Determine the role-based redirect URL
            if user.role == 'driver':
                redirect_url = '/users/driver-dashboard/'
            else:
                redirect_url = '/users/rider-dashboard/'

            return Response({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role,
                'redirect_url': redirect_url,
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def login_page(request):
    return render(request, 'users/login.html')

@api_view(['GET'])
def signup_page(request):
    return render(request, 'users/register.html')

@api_view(['GET'])
def rider_dashboard(request):
    return render(request, 'users/rider_page.html')

@api_view(['GET'])
def driver_dashboard(request):
    return render(request, 'users/driver_page.html')