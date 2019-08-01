from django.contrib import admin

# Register your models here.

from apitest.models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','status']

admin.site.register(UserInfo,UserInfoAdmin)
