from django.urls import path
from .views import * 

urlpatterns = [
    path('my-cart/', show_my_cart, name='show_my_cart'),
    path('showcart/<int:cart_id>', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_product_from_cart, name='remove_from_cart'),
    path('update_item/<int:product_id>/<str:action>/', update_item, name='update_item'),
    path('payment/', process_buy, name='process_buy'),
    path('cancel_cart/', cancel_cart, name='cancel_cart'),
    path('ticket/<int:cart_id>/', view_ticket, name='view_ticket'),
    path('payment/confirm/<int:cart_id>/', mark_as_paid, name='mark_as_paid'),
]