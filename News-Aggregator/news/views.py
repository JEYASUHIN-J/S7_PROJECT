import requests
import time
from django.shortcuts import render, redirect, get_object_or_404
from uuid import uuid4
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from news.models import Headline,EHeadline,SHeadline,PHeadline,LHeadline,ENHeadline, Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.conf import settings as django_settings
from django.contrib import messages
from django.db.models import Avg

#for scrapy
import os
import sys
import crawler_paths

# Path configuration is now handled by crawler_paths.py
path = django_settings.BASE_DIR


# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/newscrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/economycrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/sportscrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/politicscrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/lifestylecrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/entertainmentcrawler")

from newscrawler.spiders import news_spider
from economycrawler.spiders import economy_spider
from sportscrawler.spiders import sports_spider
from politicscrawler.spiders import politics_spider
from lifestylecrawler.spiders import lifestyle_spider
from entertainmentcrawler.spiders import entertainment_spider
from newscrawler.pipelines import NewscrawlerPipeline
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler,CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from newscrawler import settings as my_settings
from economycrawler import settings as economy_settings
from sportscrawler import settings as sports_settings
from politicscrawler import settings as politics_settings
from lifestylecrawler import settings as lifestyle_settings
from entertainmentcrawler import settings as entertainment_settings 
from scrapy.utils.log import configure_logging
from crochet import setup



#scrapyd = ScrapydAPI('http://localhost:6800')

def home1(request):
    return render(request, "news/starter.html")
'''
@login_required
def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context ={
            'object_list' : headlines,
    }
    return render(request, "news/home.html", context)
'''

class NewsListView(ListView):
    model = Headline
    template_name = 'news/home.html'
    paginate_by = 5
'''
@login_required
def economy_news_list(request):
    headlines = EHeadline.objects.all()[::-1]
    context ={
            'object_list' : headlines,
    }
    return render(request, "news/economy_home.html", context)
'''

class EconomyListView(ListView):
    model = EHeadline
    template_name = 'news/economy_home.html'
    paginate_by = 5
'''
@login_required
def sports_news_list(request):
    headlines = SHeadline.objects.all()[::-1]
    context ={
            'object_list' : headlines,
    }
    return render(request, "news/sports_home.html", context)
'''
class SportsListView(ListView):
    model = SHeadline
    template_name = 'news/sports_home.html'
    paginate_by = 5


class PoliticsListView(ListView):
    model = PHeadline
    template_name = 'news/politics_home.html'
    paginate_by = 5

class LifestyleListView(ListView):
    model = LHeadline
    template_name = 'news/lifestyle_home.html'
    paginate_by = 5

class EntertainmentListView(ListView):
    model = ENHeadline
    template_name = 'news/entertainment_home.html'
    paginate_by = 5


@login_required
def menu_list(request):
    return render(request, "news/topics_list.html")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape(request):
    Headline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(my_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(news_spider.NewsSpider)
    time.sleep(3)
    d=runner.crawl(news_spider.TechSpider)
    time.sleep(3)
    return redirect("../getnews/")

@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape1(request):
    EHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(economy_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(economy_spider.EconomySpider)
    time.sleep(3)
    d=runner.crawl(economy_spider.ExpressSpider)
    time.sleep(3)
    return redirect("../geteconomynews/")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape2(request):
    SHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(sports_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(sports_spider.SportsSpider)
    time.sleep(3)
    d=runner.crawl(sports_spider.HtimesSpider)
    time.sleep(3)
    return redirect("../getsportsnews/")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape3(request):
    PHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(politics_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(politics_spider.PoliticsSpider)
    time.sleep(3)
    d=runner.crawl(politics_spider.EconomicSpider)
    time.sleep(3)
    return redirect("../getpoliticsnews/")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape4(request):
    LHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(lifestyle_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(lifestyle_spider.LifestyleSpider)
    time.sleep(3)
    d=runner.crawl(lifestyle_spider.HealthSpider)
    time.sleep(3)
    return redirect("../getlifestylenews/")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape5(request):
    ENHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(entertainment_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(entertainment_spider.EntertainmentSpider)
    time.sleep(3)
    d=runner.crawl(entertainment_spider.EntrtnmentSpider)
    time.sleep(3)
    return redirect("../getentertainmentnews/")

class ArticleDetailView(DetailView):
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        article_type = self.kwargs.get('article_type', 'tech')
        if article_type == 'tech':
            return Headline.objects.all()
        elif article_type == 'economy':
            return EHeadline.objects.all()
        elif article_type == 'sports':
            return SHeadline.objects.all()
        elif article_type == 'politics':
            return PHeadline.objects.all()
        elif article_type == 'lifestyle':
            return LHeadline.objects.all()
        elif article_type == 'entertainment':
            return ENHeadline.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        article_type = self.kwargs.get('article_type', 'tech')
        
        # Get average rating
        try:
            if hasattr(article, 'comments'):
                avg_rating = article.comments.aggregate(Avg('rating'))['rating__avg']
                context['avg_rating'] = round(avg_rating) if avg_rating else 0
                context['has_comments'] = True
            else:
                context['avg_rating'] = 0
                context['has_comments'] = False
        except AttributeError:
            context['avg_rating'] = 0
            context['has_comments'] = False
        
        # Get related articles from the same source
        context['related_articles'] = self.get_queryset().filter(source=article.source).exclude(id=article.id)[:5]
        
        # Add article_type to context
        context['article_type'] = article_type
        
        return context

@login_required
def add_comment(request, article_type, article_id):
    model_map = {
        'tech': Headline,
        'economy': EHeadline,
        'sports': SHeadline,
        'politics': PHeadline,
        'lifestyle': LHeadline,
        'entertainment': ENHeadline,
    }
    
    model = model_map.get(article_type)
    if not model:
        messages.error(request, 'Invalid article type.')
        return redirect('home')
        
    article = get_object_or_404(model, id=article_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        
        if content and rating:
            try:
                from django.contrib.contenttypes.models import ContentType
                content_type = ContentType.objects.get_for_model(article.__class__)
                
                # Create comment using the generic relation
                comment = Comment(
                    content_type=content_type,
                    object_id=article.id,
                    user=request.user,
                    content=content,
                    rating=rating
                )
                
                # For backward compatibility with existing tech headlines
                if article_type == 'tech':
                    comment.headline = article
                
                comment.save()
                messages.success(request, 'Your comment has been added successfully!')
            except Exception as e:
                messages.error(request, f'Error adding comment: {str(e)}')
        else:
            messages.error(request, 'Please provide both a comment and rating.')
            
    return redirect('article_detail', article_type=article_type, pk=article_id)





