from django.urls import path

from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('news_list', views.news_list,name='news_list'),
    path('signin', views.signin,name='signin'),
    path('signup', views.signup,name='signup'),
    path('signout', views.signout, name='signout'),
    path('publish', views.publish,name='publish'),
    path('Parsing/<str:category_name>', views.Parsing, name="Parsing"),
    path('set-language/<str:lang_code>/',views.set_language, name='set_language'),
    # path('article/<str:title>/', views.view_article, name='view_article'),
    path('view_article/<str:title>/', views.view_article, name='view_article'),
]