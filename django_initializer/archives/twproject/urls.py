from django.urls import path
from twproject.views import index, load

app_name='twproject'
urlpatterns= [
    path('index/', index, name='index'),
    path('load/<int:fileid>', load, name='load')
]