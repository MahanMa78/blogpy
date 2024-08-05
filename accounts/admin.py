from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomChangeForm,CustomUserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomChangeForm
    list_display = ['id','username','email','is_staff']
    

admin.site.register(CustomUser,CustomUserAdmin)