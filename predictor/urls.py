from django.urls import path
from .views import logout_view 
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('shop/', views.shop, name='shop'),
    path('shop-detail/', views.shop_detail, name='shop_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-account/', views.my_account, name='my_account'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('predict/<str:model_type>/', views.predict_disease, name='predict_disease'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login1, name='login1'),
    path('logout/', views.logout_view, name='logout'),
]
