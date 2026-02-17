from django.urls import path
from .views import *

urlpatterns = [
    path('', display_main, name="main"),
    path('articles/', display_categories, name="articles"),
    path('information/', display_information, name="information"),
    path('promotions/', display_promotions, name="promotions"),
    path('category/<int:category_id>/', products_by_category, name='products_by_category'), 
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('promotion/<int:promo_id>/', promo_detail, name='promo_details'),
    path('search/', search_products, name='search'),
    path('backup-system/', backup_secret, name='backup_system')
]