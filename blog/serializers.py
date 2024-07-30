from rest_framework import serializers
# from .models import *

class SingleArticleSerializers(serializers.Serializer):
    title = serializers.CharField(required = True , allow_null = False , allow_blank = False , max_length = 128 )
    cover = serializers.CharField(required = True , allow_null = False , allow_blank = False , max_length = 256 )
    content = serializers.CharField(required = True , allow_null = False , allow_blank = False , max_length = 2048 )
    created_at = serializers.CharField(required = True , allow_null = False )