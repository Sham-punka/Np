from django.urls import path
from .views import *


urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),

    path('news/<int:pk>', NewsDeta.as_view(), name='news_detail'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view()),
    path('', NewsSearch.as_view(), name='news_search'),
    path('news/delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    path('news/edit/<int:pk>', NewsUpdate.as_view(), name='news_edit'),

    path('article/create', ArticleCreate.as_view()),
    path('article/edit/<int:pk>', ArticleUpdate.as_view(), name='artikle_edit'),
    path('article/delete/<int:pk>', PostDelete.as_view(), name='post_delete'),

    path('subscriptions/', subscriptions, name='subscriptions'),

    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>', Category_List_View.as_view(), name='category_list'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]