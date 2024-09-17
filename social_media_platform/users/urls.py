from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('forgot_password/', views.user_forgot_password, name='forgot_password'),
    path('index/', views.user_index, name='index'),
    path('profile/', views.user_profile, name='profile'),
    path('msg/', views.user__msg, name='msg'),
    path('notification/', views.user__notification, name='notification'),
    


    














          # copy of barber

    # path('item_list.html', views.item_list, name='item_list'),
    # path('<int:pk>/', views.item_detail, name='item_detail'),
    # path('new/', views.item_create, name='item_create'),
    # path('<int:pk>/edit/', views.item_update, name='item_update'),
    # path('<int:pk>/delete/', views.item_delete, name='item_delete'),
    # path('signin.html', views.signin, name='signin'),
]
