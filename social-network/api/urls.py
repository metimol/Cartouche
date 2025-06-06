from django.urls import include, path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('profiles', views.ProfileViewSet)
router.register('posts', views.PostViewSet)


posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('comments', views.CommentViewSet, basename='post-comments')


app_name = 'api'


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('posts/following/', views.PostsFollowing.as_view(), name="posts-following"),
    path('posts/bookmarks/', views.BookmarkedPosts.as_view(), name="posts-bookmarks"),
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
]
