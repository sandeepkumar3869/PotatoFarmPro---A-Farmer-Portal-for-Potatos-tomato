from django.urls import path
from . import views
from .views import RegisterView, LoginView, LogoutView



# urlpatterns = [
#     path('', views.index, name='home'),  # change 'index' to 'home'
#     path('services/', views.services, name='services'),
#     path('contact/', views.contact, name='contact'),
#     path('predict/<str:model_type>/', views.predict_disease, name='predict_disease'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('logout/', LogoutView, name='logout'),
# ]


# from django.urls import path
# from .views import LoginView, RegisterView, LogoutView  # Ensure you have the correct import for your views
# from . import views

# from django.urls import path
from .views import LoginView, RegisterView, LogoutView  # Import LogoutView as a class
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
    path('login/', LoginView.as_view(), name='login'),  # Login page
    
    

    path('register/', RegisterView.as_view(), name='register'),  # Register page
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout page
]

