"""
This module defines the models for the comments section of the blog.

fields:
    - author: ForeignKey to the User model
    - content: TextField
    - created_at: DateTimeField
    - updated_at: DateTimeField
    - post: ForeignKey to the Post model

methods:
    - __str__: returns the content of the comment
    - get_edit_comment_url: returns the url for editing the comment
"""

from django.db import models
from Posts.models import Post

# Create your models here.
class CommentModel(models.Model):
    """
    This class defines the model for the comments section of the blog.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # TODO: uncomment this line when you want to add the author field. (the `author` can't be disable)
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True , null=True , blank=True)

    def __str__(self):
        return self.content

    # TODO: Add edit comment for comments. (edit by author only)
    def get_edit_url(self):
        return reverse('edit_comment', args=[str(self.id)])