from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from news.models import Headline, EHeadline, SHeadline, PHeadline, LHeadline, ENHeadline
from .gemini_api import GeminiAPI

# Gemini API configuration
API_KEY = "AIzaSyC6gOxwWLT2froUzKBgilY0nJEEuV2gCqA"
MODEL_NAME = "gemini-1.5-flash"

# Initialize the Gemini API client
gemini_client = GeminiAPI(api_key=API_KEY, model_name=MODEL_NAME)

@login_required
def summarize_article(request):
    """View to summarize a news article using Gemini API"""
    if request.method == 'POST':
        article_url = request.POST.get('article_url')
        article_title = request.POST.get('article_title')
        article_content = request.POST.get('article_content')
        
        if not article_title or not article_content:
            return JsonResponse({
                'success': False,
                'error': 'Missing article title or content'
            })
        
        # Generate summary using Gemini API
        summary = gemini_client.summarize_article(article_title, article_content)
        
        return JsonResponse({
            'success': True,
            'summary': summary
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST requests are supported'
    })

@login_required
def news_insights(request, category='all'):
    """View to generate insights from news headlines"""
    # Get headlines based on category
    if category == 'general':
        headlines = Headline.objects.all()[:20]
    elif category == 'economy':
        headlines = EHeadline.objects.all()[:20]
    elif category == 'sports':
        headlines = SHeadline.objects.all()[:20]
    elif category == 'politics':
        headlines = PHeadline.objects.all()[:20]
    elif category == 'lifestyle':
        headlines = LHeadline.objects.all()[:20]
    elif category == 'entertainment':
        headlines = ENHeadline.objects.all()[:20]
    else:  # 'all' - get a mix of headlines
        headlines = list(Headline.objects.all()[:5])
        headlines.extend(list(EHeadline.objects.all()[:3]))
        headlines.extend(list(SHeadline.objects.all()[:3]))
        headlines.extend(list(PHeadline.objects.all()[:3]))
        headlines.extend(list(LHeadline.objects.all()[:3]))
        headlines.extend(list(ENHeadline.objects.all()[:3]))
    
    # Format headlines for the API
    formatted_headlines = [
        {
            'title': h.title,
            'source': h.source or 'Unknown'
        } for h in headlines
    ]
    
    # Generate insights using Gemini API
    insights_result = gemini_client.generate_insights(formatted_headlines)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(insights_result)
    
    # Render template with insights
    return render(request, 'ai_news/insights.html', {
        'insights': insights_result.get('insights', ''),
        'success': insights_result.get('success', False),
        'category': category,
        'headlines': headlines
    })

@login_required
def personalized_news(request):
    """View to provide personalized news recommendations"""
    # Get user interests (could be stored in user profile or session)
    # For now, we'll use a simple list from request parameters
    user_interests = request.GET.get('interests', '').split(',')
    user_interests = [interest.strip() for interest in user_interests if interest.strip()]
    
    if not user_interests:
        # Default interests if none provided
        user_interests = ['technology', 'world news', 'health']
    
    # Get a mix of headlines from different categories
    all_headlines = list(Headline.objects.all()[:10])
    all_headlines.extend(list(EHeadline.objects.all()[:10]))
    all_headlines.extend(list(SHeadline.objects.all()[:10]))
    all_headlines.extend(list(PHeadline.objects.all()[:10]))
    all_headlines.extend(list(LHeadline.objects.all()[:10]))
    all_headlines.extend(list(ENHeadline.objects.all()[:10]))
    
    # Format headlines for the API
    formatted_headlines = [
        {
            'title': h.title,
            'url': h.url,
            'source': h.source or 'Unknown'
        } for h in all_headlines
    ]
    
    # Get personalized recommendations
    recommended_headlines = gemini_client.personalize_recommendations(
        user_interests, formatted_headlines
    )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'recommendations': recommended_headlines
        })
    
    # Render template with recommendations
    return render(request, 'ai_news/personalized.html', {
        'recommendations': recommended_headlines,
        'interests': user_interests
    })