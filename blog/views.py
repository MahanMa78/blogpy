from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
# Create your views here.

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