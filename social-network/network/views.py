import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .utils import profile_check
from .models import *

@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def index(request):
    posts = Post.objects.all().order_by("-date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts_page": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return redirect("network:index")
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        if request.user.is_authenticated:
            return redirect("network:index")
        return render(request, "network/register.html")


@login_required(login_url="network:login")
def update_profile(request):
    profile = Profile.objects.filter(user=request.user)

    if request.method == "GET":
        return render(request, "network/updateprofile.html", {
            "profile": profile[0] if len(profile) != 0 else None
        })
    
    post = request.POST
    name = post["name"]
    image = post["image"]
    dob = post["dob"]
    bio = post["bio"]
    
    if len(profile) == 0:
        profile = Profile(user=request.user, name=name, image=image, dob=dob, bio=bio)
    else:
        profile = profile[0]
        profile.name = name
        profile.image = image
        profile.dob = dob
        profile.bio = bio
    
    profile.save()

    return redirect("network:profile", username=request.user)


@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist or Profile.DoesNotExist:
        return HttpResponse(f"<h3>Either {username} does not exist or has not created profile</h3>")
    
    posts = user.posts.all().order_by("-ispinned", "-date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile": profile,
        "posts_page": page_obj
    })


@login_required(login_url="network:login")
@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def following(request):
    following = request.user.following_list
    posts = Post.objects.filter(user__in=following).order_by("-date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts_page": page_obj
    })


@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def post(request, post_id):
    post = Post.objects.filter(pk=post_id)
    if len(post) == 0:
        return HttpResponse("<h3>Post not found</h3>")
    else:
        return render(request, "network/post.html", {
            "post": post[0],
            "comments": post[0].comments.all()
        })


@login_required(login_url="network:login")
@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def newpost(request):
    if request.method == "GET":
        return render(request, "network/newpost.html")
    
    content = request.POST["content"]
    post = Post(user=request.user, content=content)
    post.save()
    
    return redirect("network:post", post_id=post.pk)


@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
@require_POST
@csrf_exempt
def editpost(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "401",
            "response": "Log in to react"
        })
    
    data = json.loads(request.body)
    
    try:
        post = Post.objects.get(pk=post_id)
        if post.user != request.user:
            return JsonResponse({
                "status": "403",
                "response": "Forbidden, you do not have access to edit the post you have requested",
                "postId": post_id
            })
        else:
            post.content = data.get("content", "")
            post.save()
            return JsonResponse({
                "status": "201",
                "postContent": post.content
            })
    except Post.DoesNotExist:
        return JsonResponse({
            "status": "404",
            "response": "The post you are trying to access, doesn't exist",
            "postId": post_id
        })


@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
@require_POST
@csrf_exempt
def deletepost(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "401",
            "response": "Log in to perform this action"
        })
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({
            "status": "404",
            "response": "The post you are trying to access, doesn't exist",
            "postId": post_id
        })
    
    if post.user != request.user:
        return JsonResponse({
            "status": "403",
            "response": "Forbidden, you do not have access to edit the post you have requested",
            "postId": post_id
        })
    else:
        post.delete()
        return JsonResponse({
            "status": "201",
            "action": "Deleted post: " + str(post_id)
        })


@login_required(login_url="network:login")
@require_POST
@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def comment(request, post_id):
    post = Post.objects.get(pk=post_id)

    content = request.POST["content"]
    comment = Comment(content=content, post=post, user=request.user)
    comment.save()

    return redirect("network:post", post_id=post_id)


@csrf_exempt
@require_POST
def connect(request, username):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "401",
            "response": "Log in to connect"
        })
    
    user = User.objects.get(username=username)
    try:
        connection = Connection.objects.get(user=user, follower=request.user)
        connection.delete()
        return JsonResponse({
            "status": "201",
            "response": "Unfollowed"
        })
    except Connection.DoesNotExist:
        connection = Connection(user=user, follower=request.user)
        connection.save()
        return JsonResponse({
            "status": "201",
            "response": "Followed"
        })
    except:
        return JsonResponse({
            "status": "404",
            "response": "Connection does not exist"
        })


@csrf_exempt
@require_POST
def react(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "401",
            "response": "Log in to react"
        })
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({
            "status": "404",
            "response": "The post you are trying to react with, doesn't exist",
            "postId": post_id
        })
    
    try:
        reaction = Reaction.objects.get(post=post, user=request.user)
        reaction.delete()
        return JsonResponse({
            "status": "201",
            "action": "Unliked",
            "postReactionsCount": post.reactions_count
        })
    except Reaction.DoesNotExist:
        reaction = Reaction(post=post, user=request.user)
        reaction.save()
        return JsonResponse({
            "status": "201",
            "action": "Liked",
            "postReactionsCount": post.reactions_count
        })
    

@login_required(login_url="network:login")
@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def bookmarks(request):
    try:
        bookmarks = request.user.bookmarked_posts
    except:
        bookmarks = []

    paginator = Paginator(bookmarks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/bookmarks.html", {
        "posts_page": page_obj
    })


@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
@require_POST
@csrf_exempt
def bookmark(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "401",
            "response": "Log in to react"
        })
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({
            "status": "404",
            "response": "The post you are trying to bookmark, doesn't exist",
            "postId": post_id
        })
    
    try:
        bookmark = Bookmark.objects.get(post=post, user=request.user)
        bookmark.delete()
        return JsonResponse({
            "status": "201",
            "action": "Bookmark Removed"
        })
    except Bookmark.DoesNotExist:
        bookmark = Bookmark(post=post, user=request.user)
        bookmark.save()
        return JsonResponse({
            "status": "201",
            "action": "Bookmarked"
        })
    
@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
@require_POST
@csrf_exempt
def pinpost(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "401",
            "response": "Log in to perform this action"
        })
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({
            "status": "404",
            "response": "The post you are trying to access, doesn't exist",
            "postId": post_id
        })
    
    if post.user != request.user:
        return JsonResponse({
            "status": "403",
            "response": "Forbidden, you do not have access to edit the post you have requested",
            "postId": post_id
        })
    else:
        if post.ispinned:
            post.ispinned = False
            post.save()
        else:
            user_pinned_post = Post.objects.filter(user=post.user, ispinned=True)
            if len(user_pinned_post) > 0:
                user_pinned_post[0].ispinned = False
                user_pinned_post[0].save()
            post.ispinned = True
            post.save()
        return JsonResponse({
            "status": "201",
            "post": "Pinned post: " + str(post_id),
            "username": post.user.username
        })


def settings(request):
    return render(request, "network/settings.html")


@login_required(login_url="network:login")
@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def change_password(request):
    if request.method == "GET":
        return render(request, "network/change-password.html")
    
    post = request.POST
    if not request.user.check_password(post["old-password"]):
        return render(request, "network/change-password.html", {
            "message": "Incorrect old password"
        })
    
    request.user.set_password(post["new-password"])
    request.user.save()
    return redirect("network:logout")


@login_required(login_url="network:login")
@user_passes_test(profile_check, login_url="network:update_profile", redirect_field_name=None)
def delete_account(request):
    if request.method == "GET":
        return render(request, "network/delete-account.html")
    
    post = request.POST
    if not request.user.check_password(post["password"]):
        return render(request, "network/delete-account.html", {
            "message": "Incorrect password"
        })
    
    user = request.user
    user.delete()
    return redirect("network:index")
    