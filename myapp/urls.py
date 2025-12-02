from django.urls import path
from . import views


app_name = 'myapp'
urlpatterns = [
    path('campaign/', views.campaign_list, name='campaign_list'),
]