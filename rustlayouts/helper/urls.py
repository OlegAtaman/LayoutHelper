from django.urls import path
from . import views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('calculate_placement/', views.calculate_placement, name='calculate_placement'),
]