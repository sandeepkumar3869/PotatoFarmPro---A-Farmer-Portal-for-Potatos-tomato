from django.urls import path
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
from .views import logout_view 

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('my_account/', views.my_account, name='my_account'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('predict/<str:model_type>/', views.predict_disease, name='predict_disease'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login1, name='login1'),
    path('logout/', views.logout_view, name='logout'),
    path('farmer_portal/', views.farmer_portal, name='farmer_portal'),
    path('shop/', views.shop_view, name='shop'),
    path('edit_vegetable/<int:id>/', views.edit_vegetable, name='edit_vegetable'),
    path('add_to_cart/<int:vegetable_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove_from_cart/<int:vegetable_id>/', views.remove_from_cart, name='remove_from_cart'),
]
