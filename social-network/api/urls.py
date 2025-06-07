from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views


router = DefaultRouter()
router.register('profiles', views.ProfileViewSet)
router.register('posts', views.PostViewSet)
router.register('users', views.UserViewSet)


posts_router = NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('comments', views.CommentViewSet, basename='post-comments')


app_name = 'api'


urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
]
