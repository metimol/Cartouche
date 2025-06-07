from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from network.models import *
from .serializers import *

# Get all users
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'user__username']
    lookup_field = 'user'

# Get all posts and like a post
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("-date")
    filter_backends = [SearchFilter]
    search_fields = ['content', 'user__username', 'user__profile__name']
    lookup_field = 'id'

    @action(detail=True, methods=['post'], url_name="react", permission_classes=[IsAuthenticated])
    def react(self, request, id=None):
        post = self.get_object()
        reaction, created = Reaction.objects.get_or_create(user=request.user, post=post)
        if not created:
            reaction.delete()
            return Response({"message": "Like removed."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)

# Get all comments for a post and add a comment
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'id'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def get_serializer_context(self):
        user_id = self.request.user.pk if self.request.user.is_authenticated else None
        return { 'post_id': self.kwargs['post_id'], 'user_id': user_id }