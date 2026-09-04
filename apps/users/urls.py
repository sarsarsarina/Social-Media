from django.urls import path
from . import views
from .views import (
    LoginView,
    LogoutView,
    MyProfileView,
    UserProfileView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/me/", MyProfileView.as_view(), name="my_profile"),
    path("profile/<int:user_id>/", UserProfileView.as_view(), name="user_profile"),
    path('update/profile/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('follow/', views.FollowUserView.as_view(), name='follow_user'),
    path('unfollow/', views.UnfollowUserView.as_view(), name='unfollow_user'),
]