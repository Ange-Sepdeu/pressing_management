from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Add this import
from .views import apply_portfolio, portfolio_selection, process_payment, download_receipt  # Import process_payment
from .views import chat_view, marketing_promotions, add_pressing
from .views import send_message, get_messages, analytics_view






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
    path('panel/pressing-manager/', views.pressing_manager, name='pressing_manager'),
    path('panel/clients/', views.clients_panel, name='clients_panel'),
    path('panel/deliver/', views.deliver_panel, name='deliver_panel'),


    path('about_us/', views.about_us, name='about_us'),
    path('setting/', views.setting, name='setting'),
    path('customer_feedback/', views.customer_feedback, name='customer_feedback'),
    path('apply-portfolio/', views.apply_portfolio, name='apply_portfolio'),
    path('portfolio-selection/', views.portfolio_selection, name='portfolio_selection'),
    path('process-payment/', process_payment, name='process_payment'),
    path('download-receipt/<int:receipt_id>/', download_receipt, name='download_receipt'),
    path('chat/', chat_view, name='chat'),




    path('user-management/', views.user_management, name='user_management'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('about_us_dev/', views.about_us_dev, name='about_us_dev'),
    path('marketing-promotions/', marketing_promotions, name='marketing_promotions'),
    path('platform_management/add_pressing/', add_pressing, name='add_pressing'),
    path('chat/send/', send_message, name='send_message'),
    path('chat/messages/<int:user_id>/', get_messages, name='get_messages'),
    path('analytics/', analytics_view, name='analytics'),

 








]