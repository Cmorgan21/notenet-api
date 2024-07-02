from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profile/upload/<int:pk>/', views.ProfileUpdate.as_view(), name='profile-upload'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
