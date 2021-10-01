from django.urls import path
from django.contrib.auth.views import Login, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import signup, resend_otp, login_view, profile, ChangeIntoProfile, following, followers, notifications, islogin, clear_notifications

urlpatterns = [
	path(signup/', views.register, name = 'signup'),
	path('login/', views.login, name = 'login'),
