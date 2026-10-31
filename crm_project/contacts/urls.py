
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('add/', views.contact_create, name='contact_create'),
    path('<int:contact_id>/edit/', views.contact_edit, name='contact_edit'),
    path('<int:contact_id>/',views.contact_detail,name='contact_detail'),

]
