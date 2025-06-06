from rest_framework import serializers
from network.models import *


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    following = serializers.SerializerMethodField()
    following_count = serializers.IntegerField(source='user.following_count', read_only=True)
    followers_count = serializers.IntegerField(source='user.followers_count', read_only=True)
    posts_count = serializers.IntegerField(source='user.posts_count', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'is_superuser', 'is_staff', 'date_joined', 'following', 'following_count', 'posts_count', 'followers_count', 'name', 'image', 'dob', 'bio']
        read_only_fields = ['id', 'username', 'email', 'is_superuser', 'is_staff', 'date_joined', 'following', 'following_count', 'posts_count', 'followers_count']

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        if Profile.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError({"detail": "A profile already exists for this user."})
        return Profile.objects.create(user_id=user_id, **validated_data)
    
    def get_following(self, obj):
        if self.context['request'].user.is_authenticated:
            result = Connection.objects.filter(user_id=obj.user.id, follower_id=self.context['request'].user.id)
            return bool(len(result))
        return False


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "content", "date", "ispinned", "liked", "bookmarked", "reactions_count", "comments_count", "user"]
        read_only_fields = ["id", "date", "ispinned", "liked", "bookmarked", "reactions_count", "comments_count", "user"]

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return Post.objects.create(user_id=user_id, **validated_data)
    
    def get_user(self, obj):
        user = obj.user
        
        return {
            "id": user.id,
            "username": user.username,
            "name": user.profile.name if user.profile else None,
            "image": user.profile.image if user.profile and user.profile.image else None,
        }
    
    def get_liked(self, obj):
        if self.context['request'].user.is_authenticated:
            result = Reaction.objects.filter(post_id=obj.id, user_id=self.context['request'].user.id)
            return bool(len(result))
        return False
    
    def get_bookmarked(self, obj):
        if self.context['request'].user.is_authenticated:
            result = Bookmark.objects.filter(post_id=obj.id, user_id=self.context['request'].user.id)
            return bool(len(result))
        return False
    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "content", "post", "date", "user"]
        read_only_fields = ["id", "post", "date", "user"]

    def create(self, validated_data):
        post_id = self.context['post_id']
        user_id = self.context['user_id']
        return Comment.objects.create(post_id=post_id, user_id=user_id, **validated_data)

    def get_user(self, obj):
        user = obj.user
        
        return {
            "id": user.id,
            "username": user.username,
            "name": user.profile.name if user.profile else None,
            "image": user.profile.image if user.profile and user.profile.image else None,
        }