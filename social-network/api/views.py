from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from network.models import *
from .serializers import *

# Get all users
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'user__username']
    lookup_field = 'user'
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Get all posts and like a post
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("-date")
    filter_backends = [SearchFilter]
    search_fields = ['content', 'user__username', 'user__profile__name']
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        queryset = Post.objects.all().order_by("-date")
        request = getattr(self, 'request', None)
        if request is not None:
            params = getattr(request, 'query_params', None)
            if params is not None:
                limit = params.get('limit')
                if limit is not None:
                    try:
                        limit = int(limit)
                        if limit > 0:
                            queryset = queryset[:limit]
                    except ValueError:
                        pass  # ignore invalid limit
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, id=None):
        post = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        reaction, created = Reaction.objects.get_or_create(post=post, user=user)
        if not created:
            reaction.delete()
            return Response({'status': 'unliked', 'postReactionsCount': post.reactions_count})
        return Response({'status': 'liked', 'postReactionsCount': post.reactions_count})

# Get all comments for a post and add a comment
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'id'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def get_serializer_context(self):
        return { 'post_id': self.kwargs['post_id'] }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['post'] = self.kwargs['post_id']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# User viewset for creating users through API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FullUserSerializer
    http_method_names = ['get', 'post']
    permission_classes = [AllowAny]