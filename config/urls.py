from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'base.html', {"menu_name": "test"})

# можно потом сделать чтобы наследовалось от base
def catalog(request):
    return render(request, 'base.html', {})

def contacts(request):
    return render(request, 'base.html', {})

def test(request):
    return render(request, 'base.html', {"menu_name": "test"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('test1/', test, name='test1'),
    path('test1/test2/', test, name='test2'),
    path('test1/test2/test3/', test, name='test3'),

    path('about/', test, name='test4'),
    
    path('about/test1/', test, name='test5'),

    path('about/test1/test2/', test, name='test6'),
    path('about/test1/test22/', test, name='test6_2'),
    
    path('about/test1/test2/test3/', test, name='test7'),
    path('about/test1/test2/test32/', test, name='test7_2'),
    path('about/test1/test2/test33/', test, name='test7_3'),
    
    path('about/test1/test2/test3/test4/', test, name='test7'),
    
    path('about/test1/test2/test3/test4/test5/', test, name='test7'),

]
