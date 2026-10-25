from django.urls import path
from . import views



urlpatterns = [
    path('',views.company_list,name='company_list'),
    path('addcompany/',views.company_create,name='addcompany')
]