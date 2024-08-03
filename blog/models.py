from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField #bayad yek python manage.py collectstatic ham bezanim ta yekseri file ro baraye ma tanzim kone
from datetime import datetime
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

# elat inke ma az FileField be jaye ImageFild estefade kardim in bood ke FileField khali kamel tar hast
# ama ImageFiled dige niazi be validation nadare vali dar FileField bayad taarif konim
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.jpg' , '.png' ]
    # dar 2 khat bala dar ext miam va esmme on file ro tike tike mikonim ta baadan on ro check konim [1] baraye enethaye file mahsob mishe
    #va dar khat baadish miam va format hayee ke mikhahim ro dakhelesh minevisim
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatar/' , null= True , blank=True , validators=[validate_file_extension])
    description = models.CharField(max_length=512 , null=False , blank= False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Article(models.Model):
    title = models.CharField(max_length=128 , null=False , blank=False)
    cover = models.FileField(upload_to='files/article_cover/' , null=False , blank= False , validators=[validate_file_extension])
    content = RichTextField()
    created_at = models.DateTimeField(default=datetime.now , blank= False)
    category = models.ForeignKey("Category" , on_delete=models.CASCADE)
    # علت اینکه Category رو داخل ' ' گذاشتیم فریب جنگو هست
    author = models.ForeignKey(UserProfile , on_delete= models.CASCADE)
    promote = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    short_description = models.CharField(max_length=512 , null= True , blank= True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail',kwargs={'pk': self.pk})


class ActiveCommentManger(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentManger , self).get_queryset().filter(active = True)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Comment author',
    )
    
    body = models.TextField(verbose_name='Comment text')
    datetime_created = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)
    objects = models.Manager()
    active_comments_manager = ActiveCommentManger()

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.article.id])    


    def __str__(self):
        return self.author.first_name + ' ' + self.author.last_name

class Category(models.Model):
    title = models.CharField(max_length=128 , null= False, blank=False)
    cover = models.FileField(upload_to='files/category_cover/',null= True , blank= True , validators=[validate_file_extension])


    def __str__(self) :
        return self.title