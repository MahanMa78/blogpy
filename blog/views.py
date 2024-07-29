from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
# Create your views here.

class IndexPage(TemplateView):

    def get(self, request, **kwargs):
        
        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:9] #baraye inke boro va 9ta item akhar ro biar

        for article in all_articles:
            article_data.append({
                'title' : article.title,
                'cover' : article.cover.url,
                'category' : article.category.title, #baraye inke category yek kelid khareji dare be Categoey bayad barash .title bezarim
                'created_at' : article.created_at.date(),
            })

        context ={
            'article_data' : article_data,
        }

        return render(request, 'index.html',context) #request : darkhast karbar, "index.html" : safhe ke darim , context : mohtavaie ke darim
    