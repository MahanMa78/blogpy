from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomChangeForm,CustomUserCreationForm
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomChangeForm
    list_display = ['username','email','is_staff']
    

# Register your models here.
admin.site.register(CustomUser,CustomUserAdmin)