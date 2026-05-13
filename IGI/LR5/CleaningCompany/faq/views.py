from django.shortcuts import render
from faq.models import FAQ

def index(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq/faqs.html', {'faqs': faqs})