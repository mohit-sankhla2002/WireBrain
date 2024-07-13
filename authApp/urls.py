from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegistration.as_view(), name='userRegistration'),
    path('admin-register', views.AdminRegistration.as_view(), name='userRegistration'),
    path('verify-otp', views.VerifyOTP.as_view(), name='verify-otp'),
    path('verify-email', views.VerifyEmail.as_view(), name='verify-email'),
    path('login', views.UserLogin.as_view(), name='userLogin'),
    path('profile', views.UserProfile.as_view(), name='userProfile'),
    path('changePassword', views.UserChangePassword.as_view(), name='changePassword'),
    path('resetPassword', views.SendPasswordReset.as_view(), name='resetPassword'),
    path('resetUserPassword/<uid>/<token>/', views.UserPasswordReset.as_view(), name="resetPasswordLink")
]
