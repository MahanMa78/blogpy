from django.urls import path , include
from . import views


urlpatterns = [
    path('',views.IndexPage.as_view() , name='index'),
    path('contact/',views.ConatactPage.as_view() , name='contact'), #in contact ro azash be onvan masir yabi dar safahat estefadeh mikonim
    # path('article/<int:pk>/',views.ArticlePage.as_view() , name='article'),
    path("article/all/",views.AllArticleAPIView.as_view(), name='all_articles'),
    path('article/',views.SingleArticleAPIView.as_view(),name='single_article'),
    path('article/search/',views.SearchArticleAPIView.as_view(),name='search_article'),
    path('article/submit/',views.SubmitArticleAPIView.as_view(),name='submit_article'),
]