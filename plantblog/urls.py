from django.urls import path
from plantblog.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
]

