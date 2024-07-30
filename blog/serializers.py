from rest_framework import serializers
# from .models import *

class SingleArticleSerializers(serializers.Serializer):
    title = serializers.CharField(required = True , allow_null = False , allow_blank = False , max_length = 128 )
    cover = serializers.FileField( required = True ,   allow_null = False , allow_empty_file = False)
    content = serializers.CharField(required = True , allow_null = False , allow_blank = False , max_length = 2048 )
    created_at = serializers.CharField(required = True , allow_null = False )

class SubmitArticleSerializers(serializers.Serializer):
    title = serializers.CharField( required = True ,  allow_null = False , allow_blank = False , max_length = 128 )
    cover = serializers.FileField( required = True ,   allow_null = False , allow_empty_file = False)
    content = serializers.CharField(required = True , allow_null = False , allow_blank = False , max_length = 2048 )
    category_id = serializers.IntegerField(required = True , allow_null = False )
    author_id = serializers.IntegerField(required = True , allow_null =False)
    promote = serializers.BooleanField(required = True , allow_null = False)
