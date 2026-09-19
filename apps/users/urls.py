from django.urls import path
from . import views
from .views import (
    LoginView,
    LogoutView,
    MyProfileView,
    UserProfileView,
    BlockUserView,
    BlockListView
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
    path('followers/list/', views.FollowersListView.as_view(), name='followers_list'),
    path('following/list/', views.FollowingListView.as_view(), name='following_list'),
    path('follow/request/', views.FollowRequestView.as_view(), name='follow_request'),
    path('followers/count/<int:user_id>/', views.UserFollowersCountView.as_view(), name='followers_count'),
    path('following/count/<int:user_id>/', views.UserFollowingCountView.as_view(), name='following_count'),
    path('block/', views.BlockUserView.as_view(), name= 'block_user'),
    path('unblock/',views.UnblockUserView.as_view(), name='unblock_user'),
    path('block/list/',views.BlockListView.as_view(), name= 'block_list')
]