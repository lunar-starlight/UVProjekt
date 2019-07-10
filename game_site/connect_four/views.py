from django.shortcuts import redirect, get_object_or_404, reverse
from django.template import loader
from django.http import HttpResponse
from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'connect_four/index.html'

