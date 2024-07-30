from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers

class IndexPage(TemplateView):

    def get(self, request, **kwargs):
        
        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:6] #baraye inke boro va 9ta item akhar ro biar
        for article in all_articles:
            article_data.append({
                'title' : article.title,
                'cover' : article.cover.url,
                'category' : article.category.title, #baraye inke category yek kelid khareji dare be Categoey bayad barash .title bezarim
                'created_at' : article.created_at.date(),
            })


        promote_data = []
        all_promote_articles = Article.objects.filter(promote = True)
        for promote_article in all_promote_articles:
            promote_data.append({
                'category' : promote_article.category.title,
                'title' : promote_article.title,
                'author' : promote_article.author.user.first_name + " " + promote_article.author.user.last_name,
                'avatar' : promote_article.author.avatar.url if promote_article.author.avatar else None,
                'created_at' : promote_article.created_at.date(),
                'cover' : promote_article.cover.url if promote_article.cover else None,
            })



        context ={
            'article_data' : article_data, #dar asl alan 'article_data' kelid ma dar dakhel template hast
            'promote_article_data' : promote_data,
        }
        return render(request, 'index.html',context) #request : darkhast karbar, "index.html" : safhe ke darim , context : mohtavaie ke darim
    

class ConatactPage(TemplateView):
    template_name = 'page-contact.html'


# class ArticlePage(TemplateView):
#     model = Article
#     template_name = 'single-standard.html'


class AllArticleAPIView(APIView):

    def get(self , requset , format = None):
        try:
            all_articles = Article.objects.all().order_by('-created_at')[:10] #khoroji in object ha az nooe query set hast
            data = []
            for article in all_articles:
                data.append({
                    'title'      : article.title,
                    'cover'      : article.cover.url if article.cover else None,
                    'content'    : article.content,
                    'created_at' : article.created_at,
                    'category'   : article.category.title,
                    'author'     : article.author.user.first_name + ' ' + article.author.user.last_name,
                    'promote'    : article.promote,
                })

            return Response( {'data':data} , status=status.HTTP_200_OK )
        except:
            return Response( {'status':"Internal Server Error , We'll Check It Latter"} ,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        


class SingleArticleAPIView(APIView):
    
    def get(self,request,format=None):
        try:
            article_title = request.GET['article_title'] # be in ravesh migan query parameters yani toye url on prameter haie ke mikhayem pas bedim ro minevisim va albate inke in baraye data haye mammoli hast, data haye hasas ro ba POST ersal mikonan
            article = Article.objects.filter(title__contains = article_title)
            serialized_data = serializers.SingleArticleSerializers(article , many = True) #serializer daghighan kar haye tabdil on hajm az data haro be human readable anjam mide ba code kamtar , ba ArticleAPIVew moghayese shavad
            data = serialized_data.data
            # be tor kholase serializer kar tabdil object be human readable ro mikone
            return Response({'data' : data} , status=status.HTTP_200_OK)
        except:
            return Response( {'status':"Internal Server Error , We'll Check It Latter"} ,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR )