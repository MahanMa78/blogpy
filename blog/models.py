from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField #bayad yek python manage.py collectstatic ham bezanim ta yekseri file ro baraye ma tanzim kone
from datetime import datetime
from django.shortcuts import reverse

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
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatar/' , null= False , blank=False , validators=[validate_file_extension])
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
    


    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse('single_standard',args=[self.pk])
    

class Category(models.Model):
    title = models.CharField(max_length=128 , null= False, blank=False)
    cover = models.FileField(upload_to='files/category_cover/',null= True , blank= True , validators=[validate_file_extension])


    def __str__(self) :
        return self.title