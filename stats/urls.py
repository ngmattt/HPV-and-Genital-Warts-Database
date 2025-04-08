from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('region/<int:region_id>/', views.region_page, name='region_page'),
]
