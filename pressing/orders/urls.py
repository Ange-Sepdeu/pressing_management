from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Add this import




urlpatterns = [
    path('', views.home, name='home'), # Root URL routed to the home view
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout, name='logout'),
    path('panel/admin/', views.admin_panel, name='admin_panel'),
    path('panel/manager/', views.pressing_manager, name='pressing_manage_panel'),
    path('panel/clients/', views.clients_panel, name='clients_panel'),
    path('panel/deliver/', views.deliver_panel, name='deliver_panel'),

 


]