from django.urls import path
from . import views

app_name = 'ai_news'

urlpatterns = [
    path('summarize/', views.summarize_article, name='summarize_article'),
    path('insights/<str:category>/', views.news_insights, name='news_insights'),
    path('insights/', views.news_insights, name='all_insights'),
    path('personalized/', views.personalized_news, name='personalized_news'),
]