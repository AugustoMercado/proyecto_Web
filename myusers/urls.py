from django.urls import path
from .views import *

urlpatterns = [
    path('create-account/', display_create_account, name="create"),
    path('login/', display_login, name="login"),
    path('logout/', logout_account, name='logout'),
    path('history/', show_history, name='history_user'),
    path('dashboard/', owner_dashboard, name='owner_dashboard'),
]