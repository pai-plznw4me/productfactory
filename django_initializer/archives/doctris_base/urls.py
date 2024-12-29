from django.urls import path
from doctris_base.views import index, home

app_name='doctris_base'
urlpatterns = [
    path('index/', index, name='index'),
    path('home', home, name='home'),
]