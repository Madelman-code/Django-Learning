from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('secret-menu/', views.secret_menu, name='secret_menu'),
]
