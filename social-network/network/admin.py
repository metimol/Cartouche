from django.contrib import admin
from django.utils.html import format_html
from .models import *


admin.site.index_title = "Welcome to the Cartouche Admin Panel"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", 'profile_image', "email", "followers_count", "following_count", "posts_count", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("date_joined", "is_staff", "is_active")
    readonly_fields = ("followers_count", "following_count", "posts_count")
    list_per_page = 10

    def profile_image(self, obj):
        if hasattr(obj, 'profile') and obj.profile.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.profile.image)
        return "No Image"
    profile_image.short_description = "Profile Image"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", 'profile_image', "dob")
    search_fields = ("name", "user__username")
    list_per_page = 10

    def profile_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.image)
        return "No Image"
    profile_image.short_description = "Profile Image"


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("user", "follower", "date")
    search_fields = ("user__username", "follower__username")
    list_filter = ("date",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("short_content", "user", "date", "reactions_count", "comments_count", "ispinned")
    search_fields = ("content", "user__username")
    list_filter = ("ispinned", "date")
    readonly_fields = ("reactions_count", "comments_count")

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = "Post Content"


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "date")
    search_fields = ("user__username", "post__content")
    list_filter = ("date",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "short_content", "post", "date")
    search_fields = ("user__username", "content")
    list_filter = ("date",)

    def short_content(self, obj):
        return obj.content[:40] + "..." if len(obj.content) > 40 else obj.content
    short_content.short_description = "Comment"


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "date")
    search_fields = ("user__username", "post__content")
    list_filter = ("date",)

