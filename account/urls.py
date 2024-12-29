from django.contrib.auth.views import LoginView
from django.urls import path
from account.views import signup, profile, createsuperuser


app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('createsuperuser/', createsuperuser, name='createsuperuser'),

]
