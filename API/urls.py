from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("user", view=views.CreateUserView.as_view(), name="create_user"), 
    path("user/<int:pk>", view=views.RetrieveUserAPIView.as_view(), name="user_profile"), 
    path("user/<int:pk>/update", view=views.UpdateUserAPIView.as_view(), name="update_profile"),
    path("user/<int:pk>/avatar/update", view=views.UpdateAvatarAPIView.as_view(), name="update_avatar"),
    path("users", view=views.ListUsersAPIView.as_view(), name="list_users"),

    path("posts", view=views.CreateListPostView.as_view(), name="posts"),
    path("post/<int:pk>", view=views.DeleteUpdatePostView.as_view(), name="post_update_delete"),
    path("post/<int:pk>/comments", views.CreateListCommentsAPIView.as_view(), name="comments"),
    path("post/<int:pk>/like", views.CreateLikeAPIView.as_view(), name="add_like"),
    path("post/<int:pk>/unlike", views.RemoveLike.as_view(), name="remove_like"),
    path("feed", view=views.FeedAPIView.as_view(), name="user_feed"),

    path("follow", views.FollowUser.as_view(), name="follow_user"),
    path("unfollow/<int:pk>", views.UnFollowUserAPIView.as_view(), name="unfollow_user"),

    path("token", TokenObtainPairView.as_view(), name="auth_token"),
    path("token/refresh", TokenRefreshView.as_view(), name="refresh_token")
]