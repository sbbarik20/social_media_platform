from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('index/', views.user_index, name='index'),
    path('profile/', views.user_profile, name='profile'),


    














          # copy of barber

    # path('item_list.html', views.item_list, name='item_list'),
    # path('<int:pk>/', views.item_detail, name='item_detail'),
    # path('new/', views.item_create, name='item_create'),
    # path('<int:pk>/edit/', views.item_update, name='item_update'),
    # path('<int:pk>/delete/', views.item_delete, name='item_delete'),
    # path('signin.html', views.signin, name='signin'),
]
