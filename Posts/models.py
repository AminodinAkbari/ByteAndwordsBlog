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
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.utils.text import slugify
from django.urls import reverse
from django_prose_editor.fields import ProseEditorField
from Utils.html_sanitizer import PostHtmlContentSanitizer
html_sanitizer = PostHtmlContentSanitizer()

class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category , self).save(*args , **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag , self).save(*args , **kwargs)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True , blank=True)
    # TODO: sanitize and secure the content from malicious inputs. do it with bleech in save method (for admin and API will work)
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True , default=timezone.now , null=True) # if the post is published, set the published date (automatically set when the model updated)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(Category)
    # TODO: images should saved in another directory
    cover_image = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)

    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # if the post is published, set the published date
        if self.status == 'published' and not self.published:
            self.published = timezone.now()

        # sanitize post html content
        if self.content:
            self.content = html_sanitizer.sanitize_html(self.content)


        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail_view', args=[self.slug])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

# TODO: add model for images (not cover image , images for a posts)

