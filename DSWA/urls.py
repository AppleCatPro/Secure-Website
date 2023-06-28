from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_view, name='home'),

    path('accounts/logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/profile/edit', views.profile_edit, name='profile_edit'),
    path('accounts/delete/', views.delete_account_view, name='delete'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('data/edit/<int:data_id>/', views.edit_data, name='edit_data'),
    path('data/delete/<int:data_id>/', views.delete_data, name='delete_data'),
    path('data/view/<int:data_id>/', views.view_data, name='view_data'),
    path('data/add-data/', views.add_data, name='add_data'),

    path('data_updated/', views.data_updated, name='data_updated'),
    path('access_denied/', views.access_denied, name='access_denied'),


]
