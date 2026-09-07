import calendar
import logging

import pytz
from django.utils import timezone

import requests
from django.shortcuts import render, redirect
from news.models import Article
from services.models import Service
from .models import AboutCompany, Partner

logger = logging.getLogger(__name__)

def index(request):
    logger.info('Main page is loaded')

    user_tz_name = 'Europe/Minsk'
    timezone.activate(pytz.timezone(user_tz_name))
    now_local = timezone.localtime(timezone.now())
    now_utc = timezone.now()

    quote = None
    response = requests.get('https://favqs.com/api/qotd')
    if response.status_code == 200:
        data = response.json()
        quote = {
            'text': data['quote']['body'],
            'author': data['quote']['author'],
        }
    fact = None
    response = requests.get('https://catfact.ninja/fact')
    if response.status_code == 200:
        data = response.json()
        fact = {
            'fact':data['fact'],
        }
    last_article = Article.objects.filter(is_published=True).order_by('-created_at').first()
    company_info = AboutCompany.objects.last()

    preview_services = Service.objects.select_related('category')
    partners = Partner.objects.all()

    return render(request, 'main/index.html', context={'company_info' : company_info, 'last_article': last_article, 'quote': quote, 'fact': fact, 'user_tz': user_tz_name, 'now_local': now_local, 'now_utc': now_utc, 'services': preview_services, 'partners': partners})

def about(request):
    logger.info('About page is loaded')
    company_info = AboutCompany.objects.last()
    return render(request, 'main/about.html', context={'company_info': company_info})

def privacy_policy(request):
    logger.info('Privacy policy page is loaded')
    return render(request, 'main/privacy_policy.html')
