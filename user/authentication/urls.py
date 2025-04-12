from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('reset-password-request/', views.reset_password_request_view, name="reset_password_request"),
    path('reset-password/', views.reset_password_view, name="reset_password"),
    path("admin-dashboard/", views.admin_dashboard_view, name="admin_dashboard"),
]
