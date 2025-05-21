"""This model will include these fields:
- Title
- Slug: A short label for something, containing only letters, numbers, underscores or hyphens.
- Content: The main content of the post.
- Created: The date and time the post was created.
- Updated: The date and time the post was last updated(automatically set when the model updated).
- Status: The status of the post, which can be either draft or published.
- Author: A many-to-one relationship to the user model, which represents the author of the post.
- Tags: A many-to-many relationship to the tag model, which represents the tags of the post.
- Category: A many-to-one relationship to the category model, which represents the category of the post.
- Image: The image of the post.
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django_prose_editor.fields import ProseEditorField

class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
    
class Tag(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
    
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True , blank=True)
    content = ProseEditorField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True , default=timezone.now , null=True) # if the post is published, set the published date (automatically set when the model updated) (if the post is not published, set the published date to nul)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)

    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # if the post is published, set the published date
        if self.status == 'published' and not self.published:
            self.published = timezone.now()
        super(Post, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('detail_view', args=[self.slug])
    
    class Meta:
        ordering = ('-created',)    

    def __str__(self):
        return self.title