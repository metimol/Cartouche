from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from network.models import *
from .permissions import IsOwnerOrReadOnly, NoDelete
from .serializers import *
from .pagination import DefaultPagination


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'user__username']
    lookup_field = 'user'

    def get_permissions(self):
        if self.request.method == "DELETE" or self.action == "destroy":
            return [NoDelete()]
        elif self.action in ["update", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        elif self.action == "list":
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == "retrieve":
            return [IsOwnerOrReadOnly()]
        elif self.action == "create" or self.action == "connect":
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def connect(self, request, user=None):
        profile = self.get_object()
        target_user = profile.user

        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        connection = Connection.objects.filter(user=target_user, follower=request.user).first()

        if connection:
            connection.delete()
            return Response({"detail": "Unfollowed successfully."}, status=status.HTTP_200_OK)
        else:
            Connection.objects.create(user=target_user, follower=request.user)
            return Response({"detail": "Followed successfully."}, status=status.HTTP_201_CREATED)
        
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def following(self, request, user=None):
        profile = self.get_object()
        target_user = profile.user

        following_list = target_user.following_list
        data = [{"id": user.id, "username": user.username, "name": user.profile.name, "image": user.profile.image } for user in following_list]
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def followers(self, request, user=None):
        profile = self.get_object()
        target_user = profile.user

        followers_list = target_user.followers_list
        data = [{"id": user.id, "username": user.username, "name": user.profile.name, "image": user.profile.image } for user in followers_list]
        return Response(data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("-date")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_id']
    search_fields = ['content', 'user__username', 'user__profile__name']
    pagination_class = DefaultPagination
    lookup_field = 'id'

    @action(detail=True, methods=['post'], url_name="react", permission_classes=[IsAuthenticated])
    def react(self, request, id=None):
        post = self.get_object()
        reaction, created = Reaction.objects.get_or_create(user=request.user, post=post)

        if not created:
            reaction.delete()
            return Response({"message": "Like removed."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_name="bookmark", permission_classes=[IsAuthenticated])
    def bookmark(self, request, id=None):
        post = self.get_object()
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

        if not created:
            bookmark.delete()
            return Response({"message": "Bookmark removed."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "Post bookmarked."}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_name="pin", permission_classes=[IsAuthenticated])
    def pin(self, request, id=None):
        post = self.get_object()

        if post.user != request.user:
            return Response(
                {"message": "You can only pin or unpin your own posts."},
                status=status.HTTP_403_FORBIDDEN
            )

        if post.ispinned:
            post.ispinned = False
            post.save()
            return Response(
                {"message": "The post has been unpinned."},
                status=status.HTTP_200_OK
            )
        else:
            old_pinned_post = Post.objects.filter(user=request.user, ispinned=True).first()
            if old_pinned_post:
                old_pinned_post.ispinned = False
                old_pinned_post.save()

            post.ispinned = True
            post.save()

            message = "The post has been pinned"
            message += ", and the previously pinned post was unpinned." if old_pinned_post else "."

            return Response({"message": message}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        elif self.action == "list":
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == "retrieve":
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()
    

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])
    
    def get_serializer_context(self):
        return { 'post_id': self.kwargs['post_id'], 'user_id': self.request.user.id }
    
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        elif self.action == "list":
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == "retrieve":
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()


class PostsFollowing(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        following = self.request.user.following_list
        return Post.objects.filter(user__in=following).order_by("-date")
    

class BookmarkedPosts(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        return self.request.user.bookmarked_posts