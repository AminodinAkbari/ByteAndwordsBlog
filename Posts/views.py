"""
This file contains the views for the Posts app. one of the views is FBV (Function Based View) and the other one is CBV (Class Based View). this isn't have any reason I just wanted to use both of them.
"""

# Posts/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from Posts.models import Post
from Comment.models import CommentModel
# Import our new serializers
from Posts.serializer import PostSerializer, PostDetailSerializer
from Posts.pagination import NormalResultsPagination

# TODO: In this class have repeated "status=published" for showing posts.try this method be DRY.
class PostViewSet(viewsets.ViewSet):

    """ This view will do these things : list all posts, retrieve by slug ,list posts accourding to a tag and create new posts.
    """

    def list(self, request):
        """
        Return a list of all posts.

        This endpoint supports optional pagination through the `page_size` query parameter.
        - If `page_size` is provided in the request URL (e.g. `?page_size=10`), results
          are paginated using `NormalResultsPagination`, and the response will include
          pagination metadata (count, next, previous, results).
        - If `page_size` is not provided, all posts are returned in a single response
          without pagination.
        - ViewSet not support default pagination in settings file.
        """
        queryset = Post.objects.filter(status='published')
        paginator = NormalResultsPagination()

        pages = paginator.paginate_queryset(queryset , request , view=self)

        if pages is not None:
            serializer = PostSerializer(pages , many='published')
            return paginator.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset , many = True)
        return Response(serializer.data)

    def retrieve(self , request , slug):
        """ Get a post accourding to requested slug. """
        queryset = Post.objects.filter(status='published')
        retrieved_post = get_object_or_404(queryset , slug = slug)
        serializer = PostSerializer(retrieved_post)
        return Response(serializer.data)

    def retrieve_posts_by_tag(self , request, *args, **kwargs):
        """Reveive all posts those have requested tag. """
        tag = kwargs["tag"]
        queryset = Post.objects.filter(tags__slug = tag, status='published')
        serializer = PostSerializer(queryset , many = True)
        return Response(serializer.data)

