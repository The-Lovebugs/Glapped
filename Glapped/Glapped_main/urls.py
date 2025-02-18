from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createlisting/', views.createListing, name='create'),
    path('<int:pk>/', views.product_page, name='product_page'),
]