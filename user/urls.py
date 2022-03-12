from django.urls import path
from user import views 

from typing import List

app_name = 'user'

urlpatterns: List[path] = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('manage/', views.ManageUserView.as_view(), name='manage'),
]
