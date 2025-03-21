from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/',views.account,name='account'),
    path('createlisting/', views.createListing, name='createListing'),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.product_page, name='product_page'),
    path('leaderboard/', views.leaderBoard, name='leaderboard'),
    path('buy/<int:pk>', views.buy, name='buy'),
    path('bid/<int:pk>/', views.place_bid, name='place_bid')
]