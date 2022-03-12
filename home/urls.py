from django.urls import path
from home import views

from typing import List

app_name: str = 'home'

urlpatterns: List[path] = [
    path('', views.homeView, name='home'),
]