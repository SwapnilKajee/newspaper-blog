from django.urls import path
from personal_blog import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("drafts/", views.DraftListView.as_view(), name="draft-list"),
    path("post-create/", views.PostCreateView.as_view(), name="post-create"),
    path("post-delete/<int:pk>/", views.PostDeleteView.as_view(), name="post-delete"),
    path("post-update/<int:pk>/", views.PostUpdateView.as_view(), name="post-update"),
    path("post-publish/<int:pk>/", views.PostPublishView.as_view(), name="post-publish"),
    path("post-by-tag/<int:tag_id>/", views.PostByTag.as_view(), name="post-by-tag"),
    path("post-by-category/<int:cat_id>/", views.PostByCategory.as_view(), name="post-by-category"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("newsletter", views.NewsLetterView.as_view(), name="newsletter"),
    path("post-serach/", views.PostSearchView.as_view(), name="post-search"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("comment-create/", views.CommentCreateView.as_view(), name="comment-create")
]
