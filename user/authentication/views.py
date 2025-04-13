from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout, authenticate
from .models import UserToken, UserProfile
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.

class CreateUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {
                    'error': 'username password boş geçilemez'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {
                    'error':'kullanıcı adı alınmış'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        new_user = UserProfile(
            user=user
        )
        new_user.save()

        response = {
            'id':new_user.id,
            'username':new_user.user.username
        }
        return Response(
            {
                'user':response
            },
            status=status.HTTP_200_OK
        )
    
    def get(self, request):
        users = UserProfile.objects.all()
        
        response = []
        for user in users:
            temp = {
                'id': user.user.id,
                'username': user.user.username
            }
            response.append(temp)
        
        return Response(
            {
                'users': response
            },
            status=status.HTTP_200_OK
        )

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            _user = User.objects.get(
                username=username
            )
            if not _user.is_active:
                return Response(
                    {
                        'message': 'Hesap aktif değil'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {
                    'error': 'Kullanıcı bulunamadı'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        user = authenticate(
            request=request,
            username=username,
            password=password
        )
        
        if user is not None:
            refresh = RefreshToken.for_user(user)

            try:
                _token = UserToken.objects.get(
                    user=user
                )
                _token.delete()
            except UserToken.DoesNotExist:
                pass
            
            _token = UserToken(
                user=user,
                refresh=str(refresh),
                access=str(refresh.access_token)
            )
            _token.save()

            return Response(
                {
                    'refresh_token': _token.refresh,
                    'access_token': _token.access
                }
            )
        else:
            return Response(
                {
                    'error': 'Kullanıcı adı veya şifre yanlış'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserLogoutView(APIView):
    def post(self,request):
        try:
            token = UserToken.objects.get(
                access = request.data.get('access_token')
            )
        except:
            return Response(
                {
                    'error': 'token yok'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        token.delete()
        login_url = reverse('user:login')

        return Response(
            {
                'message':'başarıyla çıkış yaptın',
                'redirect_url': login_url
            },
            status=status.HTTP_200_OK
        )