from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('/about/', views.about, name="AboutShop"),
    path('/contact/', views.contact, name="Contact"),
    path('/tracker/', views.track, name="Tracker"),
    path('/search/', views.search, name="Search"),
    path('/products/<int:id>', views.viewpro, name="ViewPro"),
    path('/checkout/', views.checkout, name="Check"),
]
