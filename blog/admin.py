from django.contrib import admin

# Register your models here.
from .models import *

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['id','user' , 'avatar' , 'description']

# admin.site.register(UserProfile,UserProfileAdmin)


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title' , 'content']
    list_display = ['title' , 'category' , 'created_at']

admin.site.register(Article , ArticleAdmin)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title' , 'cover']

admin.site.register(Category,CategoryAdmin )


class CommentInLine(admin.ModelAdmin):
    model = Comment
    list_display = ['author' , 'body' , 'active']   
    

admin.site.register(Comment , CommentInLine )