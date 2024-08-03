from django.urls import path , include
from . import views


urlpatterns = [
    path('',views.IndexPage.as_view() , name='home'),
    path('article/<int:pk>/',views.ArticlePage.as_view() , name='article_detail'),
    path('contact/',views.ConatactPage.as_view() , name='contact'), #in contact ro azash be onvan masir yabi dar safahat estefadeh mikonim
    path("article/all/",views.AllArticleAPIView.as_view(), name='all_articles'),
    path('article/',views.SingleArticleAPIView.as_view(),name='single_article'),
    path('article/search/',views.SearchArticleAPIView.as_view(),name='search_article'),
    path('article/submit/',views.SubmitArticleAPIView.as_view(),name='submit_article'),
    path('article/update-cover/',views.UpdateArticleAPIView.as_view(),name='update_article'),
    path('article/delete/',views.DeleteArticleAPIView.as_view(),name='delete_article'),
]