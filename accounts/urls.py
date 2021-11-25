from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .forms import PwdResetConfirmForm, PwdResetForm




app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/password_reset.html", success_url='password_reset_successful', email_template_name='account/password_reset_email.html',form_class=PwdResetForm), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),name="password_reset_confirm"),
    path('password_reset/password_reset_successful',
         TemplateView.as_view(template_name="account/password_reset_done.html"), name='password_reset_successful'),
    path('accounts/reset/done/',
         TemplateView.as_view(template_name="account/reset_status.html"), name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete_user/', views.delete_profile, name='delete_profile'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/delete_profile.html"), name='confirm_delete'),
    path('order/checkout/', views.checkout, name='payment'),


    path('password_reset/password_reset_successful/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/password_reset_email.html"), name='password_reset_email'),
]




