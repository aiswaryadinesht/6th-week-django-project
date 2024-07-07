from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path("home/", views.home, name='home'),
    path("logout/", views.user_logout, name='logout'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('admin_panel/', views.admin_panel_view, name='admin_panel'),
    path('admin_panel/search/', views.user_search_view, name='user_search'),
    path('admin_panel/edit/<int:user_id>/', views.user_edit_view, name='edit_user'),
    path('admin_panel/delete/<int:user_id>/', views.user_delete_view, name='delete_user'),
    path('admin_panel/user/<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('admin_panel/change_password/<int:user_id>/', views.user_password_change_view, name='change_password'),
    path('admin_panel/create_user/', views.create_user, name='create_user'),
    path("logout1/", views.admin_logout, name='logout1'),
    
]

