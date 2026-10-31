from django.urls import path
from . import views

urlpatterns = [
    path('',views.company_list,name='company_list'),
    path('addcompany/',views.company_create,name='addcompany'),
    path('<int:company_id>/edit/', views.company_edit, name='company_edit'),
    path('<int:company_id>/', views.company_detail, name='company_detail'),
]