from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from django.views import generic

class IndexPage(TemplateView):

    def get(self, request, **kwargs):
        
        article_data = []
        all_articles = Article.objects.filter(is_active = True).order_by('-created_at')[:12] #baraye inke boro va 9ta item akhar ro biar
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
        return render(request, 'articles_list.html',context) #request : darkhast karbar, "index.html" : safhe ke darim , context : mohtavaie ke darim
    

class ConatactPage(TemplateView):
    model = UserProfile
    template_name = 'contact_page.html'
    context_object_name = 'contact'


class ArticlePage(generic.DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
    
    


class AllArticleAPIView(APIView):
    # baraye search kardanesh bayad benevisim : http://localhost:8000/article/all/
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
        


class SingleArticleAPIView(APIView):#baraye zamani estefade mishe ke bekhahim yek maghale ro search konim
    # baraye search kardanesh bayad benevisim : http://localhost:8000/article/?article_title=فوتبال
    
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
        

class SearchArticleAPIView(APIView): #baraye zamani estefade mishe ke bekhahim yek kalame ya matn ro dakhele article ha search konim
    # baraye search kardanesh bayad benevisim : http://localhost:8000/article/search/?query=لورم ایپسوم
    def get(self , request , format=None):
        try:
            from django.db.models import Q #baraye anjam query haye pishrafte dar django az Q estefade mikonim

            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            data = []
            for article in articles:
                data.append({
                    'title'      : article.title,
                    'cover'      : article.cover.url if article.cover else None,
                    'content'    : article.content,
                    'created_at' : article.created_at,
                    'category'   : article.category.title,
                    'author'     : article.author.user.first_name + ' ' + article.author.user.last_name,
                    'promote'    : article.promote,
                })

            return Response({'data' : data} , status=status.HTTP_200_OK)

        except:
            return Response( {'status':"Internal Server Error , We'll Check It Latter"} ,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        
class SubmitArticleAPIView(APIView):
    # baraye estefade az inke ba api yek maghale benevisim bayad az : http://localhost:8000/article/submit/ estefade konim
    def post(self , requset , format = None):
        try:
            serializer = serializers.SubmitArticleSerializers(data=requset.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = requset.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status':'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(id = author_id)
            # ham category va ham author ro bayad object hasho begirim shon darim azash id migirm
            author = UserProfile.objects.get(user = user)
            category = Category.objects.get(id = category_id)

            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            #hala chon balatar ma az category va author object hashon ro gereftim inja estefade mikonim
            article.author = author
            article.category = category
            article.promote = promote
            article.save()
        #NOKTE: ma az 'created_at' estefade nemikonim chon ke created_at meghdar default= datetime.now ro dare yani zamani ke object yek 
        #edame: maghale sakhte mishe created_at meghdar pishfarz zamani ke maghale dare sakhte mishe ro migire va ma lazem nist zamani ke darim ba api kar mikonim meghdare created_at ro bedim
            return Response({'status':'OK'},status=status.HTTP_200_OK)
        except:
            return Response( {'status':"Internal Server Error , We'll Check It Latter"} ,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        

class UpdateArticleAPIView(APIView):
    # baraye update cover az in link vared mishavim :  http://localhost:8000/article/update-cover/
    def post(self , request , format= None):
        try: 
            serializer = serializers.UpdateArticleCoverSerializers(data=request.data)

            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response({'status':'Bad Request.'} , status=status.HTTP_400_BAD_REQUEST)
            


            Article.objects.filter(id= article_id).update(cover=cover)

            return Response({'status':'OK'} , status=status.HTTP_200_OK)
        except:
            return Response( {'status':"Internal Server Error , We'll Check It Latter"} ,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        

class DeleteArticleAPIView(APIView):
    #baraye inke bekhahim hazf konim bayad az link : http://localhost:8000/article/delete/
        def post(self, request , format=None):
            try:
                serializer = serializers.DeleteArticleSerializers(data = request.data)

                if serializer.is_valid():
                    article_id = serializer.data.get('article_id')
                else:
                    return Response({'status':"Bad Request"} , status=status.HTTP_400_BAD_REQUEST)
                
                Article.objects.filter(id = article_id ).delete()

                return Response({'status':'OK'} , status=status.HTTP_200_OK)
            
            except:
                return Response( {'status':"Internal Server Error , We'll Check It Latter"} ,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR )