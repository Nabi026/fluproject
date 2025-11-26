from django.urls import path
from . import views

app_name = 'flu'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('prevention/', views.prevention, name='prevention'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('contact/', views.contact, name='contact'),
]