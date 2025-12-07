from django.urls import path
from . import views
from .views import PostByTagListView

app_name = "blog"

urlpatterns = [
    # ----- Blog post views -----
    path("", views.index, name="index"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),

    # ----- Post CRUD views -----
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),

    # ----- Comment CRUD -----
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),

    # ----- Authentication views -----
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),

    # ------- Search functionality -------
    path("search/", views.search_posts, name="search_posts"),

    # --------- Filter by tag ---------
    path("tags/<str:tag_name>/", views.posts_by_tag_view, name="posts_by_tag"),
    
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts_by_tag"),
]