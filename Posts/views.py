"""
This file contains the views for the Posts app. one of the views is FBV (Function Based View) and the other one is CBV (Class Based View). this isn't have any reason I just wanted to use both of them.
"""

# Posts/views.py
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
    GenericViewSet,
    ModelViewSet
)

from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from Posts.models import Post,PostImages

from Posts.serializer import (
    PostSerializer,
    PostsImagesSerializer,
    PostDetailSerializer
)
from Posts.pagination import NormalResultsPagination

from Posts.models import Post

from Blog.custome_permissions import IsAdminOrReadOnly
class ALLPostsCustomMixins:
    """Custom Mixin to filter published posts."""
    def get_queryset(self):
        return Post.objects.all()
    
class SlugLookupCustomMixin:
    """Custom Mixin to use slug as lookup field."""
    lookup_field = "slug"
    
class PublishedPostBySlugMixin(ALLPostsCustomMixins, SlugLookupCustomMixin):
    """Custom mixin to retrieve a published post by slug."""
    ...

class PublishedPostViewSet(PublishedPostBySlugMixin, ReadOnlyModelViewSet):
    """ This view listing all published posts. """
    serializer_class = PostSerializer
    pagination_class = NormalResultsPagination

    
class CRUDPostsViewset(
    PublishedPostBySlugMixin,
    ModelViewSet
):
    """ create,read,update and delete posts models."""
    serializer_class = PostDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    

class PostsImagesView(
    GenericViewSet,
    CreateModelMixin,        # POST
    RetrieveModelMixin,      # GET /pk/
    UpdateModelMixin,        # PUT/PATCH /pk/
    DestroyModelMixin,       # DELETE /pk/
    ListModelMixin           # GET /
):
    """ This viewset provides CRUD operations for PostImages. """
    queryset = PostImages.objects.all()
    serializer_class = PostsImagesSerializer
    permission_classes = [IsAdminOrReadOnly]

class PostsByTagView(ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = NormalResultsPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug = self.request.query_params.get('tag')
        if not slug:
            return Post.objects.none()
        return Post.objects.filter(status='published', tags__slug=slug).distinct()
