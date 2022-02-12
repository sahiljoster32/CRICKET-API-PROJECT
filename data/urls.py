from django.urls import path
from data import views

app_name = 'data'

urlpatterns = [
    path('get/', views.CricketDataRetrieveAPI.as_view(), name='get'),
]
