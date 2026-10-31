
from django.urls import path
from . import views

urlpatterns = [
    path('', views.deal_list, name='deal_list'),
    path('new/', views.deal_create, name='deal_create'),
    path('<int:pk>/edit/', views.deal_edit, name='deal_edit'),
    path('<int:pk>/update-stage/',views.update_deal_stage,name='update_deal_stage'),
    path('<int:deal_id>/', views.deal_detail, name='deal_detail'),
]
