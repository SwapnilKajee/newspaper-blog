from django.db import models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True   # doesnot create table for TimeStampModel
 
 
class Category(TimeStampModel):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Tag(TimeStampModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(TimeStampModel):
    STATUS_CHOICES = [("published", "published"), ("unpublished", "unpublished")]
    title = models.CharField(max_length=256)
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    tag = models.ManyToManyField(Tag)
    content = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    published_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unpublished")
    views_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

    # Fat models
    @property
    def latest_comments(self):
        comments = Comment.objects.filter(post=self).order_by("-created_at")
        return comments


class NewsLetter(TimeStampModel):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Contact(TimeStampModel):
    message = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=256)

    def __str__(self):
        return self.subject

class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    def __str__(self):
        return self.description[:100]

