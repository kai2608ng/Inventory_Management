from django.urls import path
from .views import login_page, new_user_page, logout

urlpatterns = [
    path('', login_page, name = "login_page"),
    path('new_user/', new_user_page, name = "new_user_page"),
    path('logout/', logout, name = 'logout'),
]