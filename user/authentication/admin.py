from django.contrib import admin
from .models import UserProfile, UserToken

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user'
    ]
    class Meta:
        model = UserProfile

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        # 'key',
        'last_activity'
    ]
    class Meta:
        model = UserToken