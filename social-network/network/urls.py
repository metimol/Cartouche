from django.urls import path

from . import views

app_name = 'network'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update-profile", views.update_profile, name="update_profile"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("newpost", views.newpost, name="newpost"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("profile/<str:username>/connect", views.connect, name="connect"),
    path("posts/<int:post_id>/react", views.react, name="react"),
    path("posts/<int:post_id>/edit", views.editpost, name="editpost"),
    path("posts/<int:post_id>/delete", views.deletepost, name="deletepost"),
    path("posts/<int:post_id>/pin", views.pinpost, name="pinpost"),
    path("bookmarks", views.bookmarks, name="bookmarks"),
    path("posts/<int:post_id>/bookmark", views.bookmark, name="bookmark"),
    path("settings", views.settings, name="settings"),
    path("settings/change-password", views.change_password, name="change-password"),
    path("settings/delete-account", views.delete_account, name="delete-account"),
]
