from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, ChangePasswordAPIView,UserProfileView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
  path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
]

