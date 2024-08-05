from django.db import models
from django.contrib.auth.models import AbstractUser , Group, Permission

class CustomUser(AbstractUser):
    birth = models.DateField(null=True ,blank=True )
    email = models.EmailField(null=True , blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_user_permissions',  
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )