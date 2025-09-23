"""
This file contains the views for the Posts app. one of the views is FBV (Function Based View) and the other one is CBV (Class Based View). this isn't have any reason I just wanted to use both of them.
"""

# Posts/views.py
from rest_framework import generics, permissions
from django.db.models import Prefetch
from Posts.models import Post
from Comment.models import CommentModel
# Import our new serializers
from Posts.serializer import PostSerializer, PostDetailSerializer


class PostListAPIView(generics.ListAPIView):
    """
    API View to list all posts (only published posts).
    """
    # We only want to show published posts, just like in your original view
    queryset = Post.objects.filter(status = 'published')
    serializer_class = PostSerializer
    # Anyone can view the list of posts
    permission_classes = [permissions.AllowAny]

class PostDetailRetrieveAPIView(generics.RetrieveAPIView):
    """
    Api view to see a post detail using it's slug (only published posts)
    """
    queryset = Post.objects.filter(status = 'published')
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]

    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        available_comments = CommentModel.objects.filter(is_approved = True)
        print("Comments :" ,available_comments)

        return queryset.prefetch_related(
            Prefetch('comments', queryset = available_comments)
        )


    #     return context
