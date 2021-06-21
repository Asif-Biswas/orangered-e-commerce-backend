from django.urls import path
from . import views
#from .views import ChangePasswordView
urlpatterns = [
    #path('', views.home, name='home'),
    #path('a/', views.access, name='access'),
    path('handleLikes/', views.handleLike, name='handleLike'),
    path('getLikes/', views.getLikes, name='getLikes'),
    path('forYou/', views.forYou, name='forYou'),
    path('getCategoryName/', views.getCategoryName, name='getCategoryName'),
    path('getProduct/', views.getProduct, name='getProduct'),
    path('productDetails/<str:pk>/', views.productDetails, name='productDetails'),
    path('getCategoryProduct/', views.getCategoryProduct, name='getCategoryProduct'),
    path('getCompanyProduct/', views.getCompanyProduct, name='getCompanyProduct'),
    path('addToCart/<str:pk>/', views.addToCart, name='addToCart'),
    #path('addToCartForSession/<str:pk>/', views.addToCartForSession, name='addToCartForSession'),
    path('myCartDetails/', views.myCartDetails, name='myCartDetails'),
    path('deleteCartItem/<str:pk>/', views.deleteCartItem, name='deleteCartItem'),
    path('undoDeletedCartItem/<str:pk>/', views.undoDeletedCartItem, name='undoDeletedCartItem'),
    path('myDetails/', views.myDetails, name='myDetails'),
    path('purchase/', views.purchase, name='purchase'),
    path('myAllCartItems/', views.myAllCartItems, name='myAllCartItems'),
    path('youMayLikeOnCart/', views.youMayLikeOnCart, name='youMayLikeOnCart'),
    path('totalItemInCart/', views.totalItemInCart, name='totalItemInCart'),
    path('increaseQuantity/<str:pk>/', views.increaseQuantity, name='increaseQuantity'),
    path('decreaseQuantity/<str:pk>/', views.decreaseQuantity, name='decreaseQuantity'),
    path('search/<str:str>/', views.search, name='search'),

    

    #path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    
]