from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse(200)

def home(request):
    return render(request, template_name='doctris_base/base.html')