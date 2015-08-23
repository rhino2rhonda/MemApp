from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView


# Create your views here.
class HomeView(TemplateView):
    template_name = 'common/index.html'
    
