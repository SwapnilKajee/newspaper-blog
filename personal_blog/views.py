from multiprocessing import context
from string import Template
from typing import List
from unicodedata import category
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from personal_blog.forms import CommentForm, ContactForm, NewsLetterForm, PostForm
from personal_blog.models import Post, Category, Tag
from django.utils import timezone
from personal_blog.forms import PostForm
from datetime import timedelta

from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

one_week_ago = timezone.now() - timedelta(days=7)
PAGINATE_BY = 1

class HomePageView(ListView):
    model = Post
    template_name = "aznews/index.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status="published").order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_posts'] = Post.objects.filter(status="published").order_by("-views_count")[:3]
        context['most_viewed'] = (Post.objects.filter(status="published").order_by("-views_count").first())  #getting most viewed single post
        context["weekly_top_posts"] = Post.objects.filter(status="published",published_at__gte=one_week_ago).order_by("-views_count")[:7]
        context['recent_posts'] = Post.objects.filter(status="published").order_by("-created_at")[:5]
        context["top_categories"] = Category.objects.all()[:4]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/main/blog/detail/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        obj.views_count += 1
        obj.save()
        # next and previous posts
        context = super().get_context_data(**kwargs)
        context["previous_post"] = Post.objects.filter(id__lt=obj.id, status="published").order_by("-id").first()
        context["next_post"] = Post.objects.filter(id__gt=obj.id, status="published").order_by("id").first()
        return context



class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "aznews/main/blog/post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=True)
    paginate_by = PAGINATE_BY


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("draft-list")
    def form_valid(self, form):
        form.instance.author = self.request.user  #logged in user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect("home")

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("home")


class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.status = "published"
        post.published_at = timezone.now()
        post.save()
        return redirect("home")
        

# class PostByTag(View):
#     template_name = "aznews/main/blog/post_list.html"
#     def get(self, request, tag_id, *args, **kwargs):
#         categories = Category.objects.all()
#         posts = Post.objects.filter(tag=tag_id)
#         return render(request, self.template_name, {"posts":posts, "categoreis":categories})

class PostByTag(ListView):
    model = Post
    template_name = "aznews/main/blog/post_list.html"
    context_object_name = "posts"
    paginate_by = PAGINATE_BY
    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(status = "published", tag=self.kwargs["tag_id"])
        return queryset


# class PostByCategory(View):
#     template_name = "aznews/main/blog/post_list.html"
#     def get(self, request, cat_id, *args, **kwargs):
#         posts = Post.objects.filter(category=cat_id)
#         return render(request, self.template_name, {"posts":posts})


class PostByCategory(ListView):
    model = Post
    template_name = "aznews/main/blog/post_list.html"
    context_object_name = "posts"
    paginate_by = PAGINATE_BY
    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(status = "published", category=self.kwargs["cat_id"])
        return queryset



class ContactView(View):
    template_name = "aznews/contact.html"
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {"categoreis":categories})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully submitted the form. We will contact you soon.")
        else:
            messages.error(request, "Sorry Something went wrong.")
        return render(request, self.template_name)


class NewsLetterView(View):
    form_class = NewsLetterForm

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":   # is this an ajax request?
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True}, status=200)
        return JsonResponse({"success": False}, status=400)


class PostSearchView(View):
    template_name = 'aznews/main/blog/post_search.html'

    # def get(self, request, *args, **kwargs):
    #     posts = Post.objects.filter(status="published")
    #     return render(request, self.template_name, {"posts":posts})

    def get(self, request, *args, **kwargs):
        query = request.GET["query"]
        posts_list = Post.objects.filter( (Q(title__icontains=query) | Q(content__icontains=query)) & Q(status="published")).order_by("-published_at")      
        # pagination starts
        page = request.GET.get("page", 1)
        paginator = Paginator(posts_list, PAGINATE_BY)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        # pagination ends
        return render(request, self.template_name, {"page_obj":posts, "query":query})


class AboutView(TemplateView):
    template_name = "aznews/about.html"


class CommentCreateView(View):
    form_class = CommentForm
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        post_id = request.POST["post"]
        if form.is_valid():
            form.save()
        return redirect("post-detail", post_id)

        
