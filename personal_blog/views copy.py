from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from personal_blog.forms import PostForm
from personal_blog.models import Post
from django.utils import timezone
from personal_blog.forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).order_by('-published_at')  #ORM -> object relational mapping
    return render(
        request,
        "post_list.html",
        {"posts": posts},
    )

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "post_detail.html", {"post":post})

@login_required
def draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True)
    return render(
        request,
        "post_list.html",
        {"posts": posts},
    )

@login_required
def post_create(request):
    if request.method == "POST":
        print(request.POST)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user      #logged in user
            post.save()
            return redirect("post-list")
    form = PostForm()
    return render(request, "post_create.html", {"form":form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("post-list")

@login_required
def post_update(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post-detail", pk=pk)
    else:
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, "post_create.html", {"form":form})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_at = timezone.now()
    post.save()
    return redirect("post-list")



