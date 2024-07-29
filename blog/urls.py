from django.urls import path , include
from . import views


urlpatterns = [
    path('',views.IndexPage.as_view() , name='index'),
    path('contact/',views.ConatactPage.as_view() , name='contact') #in contact ro azash be onvan masir yabi dar safahat estefadeh mikonim
]