from django.urls import path
from .views import CreateUserView, UserLoginView, UserLogoutView, frontend_view

app_name = 'user'

urlpatterns = [
    path('', frontend_view, name='frontend'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]