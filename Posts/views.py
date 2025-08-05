"""
This file contains the views for the Posts app. one of the views is FBV (Function Based View) and the other one is CBV (Class Based View). this isn't have any reason I just wanted to use both of them.
"""

# Posts/views.py
from rest_framework import generics, permissions
from Posts.models import Post
# Import our new serializers
from Posts.serializer import PostSerializer
from django.utils import timezone


class PostListAPIView(generics.ListAPIView):
    """
    API View to list all posts (draft or published).
    """
    # We only want to show published posts, just like in your original view
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Anyone can view the list of posts
    permission_classes = [permissions.AllowAny]