"""
This file contains the views for the Posts app. one of the views is FBV (Function Based View) and the other one is CBV (Class Based View). this isn't have any reason I just wanted to use both of them.
"""
from django.db.models import F, Q
from django.db.models.functions import Greatest

from django.contrib.postgres.search import SearchQuery, SearchRank
from django.contrib.postgres.search import SearchHeadline
from django.contrib.postgres.search import TrigramSimilarity

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
    PostDetailSerializer,
    TagsSerializer
)
from Posts.pagination import NormalResultsPagination
from Posts.models import Post, Tag
from Blog.custome_permissions import IsAdminOrReadOnly

class SearchPostsView(ReadOnlyModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        q = (self.request.query_params.get("q") or "").strip()

        qs = Post.objects.filter(status="published")

        if not q:
            return qs.order_by("-published")

        # 1) FTS query parsing: "websearch" feels natural for users
        search_query = SearchQuery(q, config="english", search_type="websearch")

        # 2) Rank from stored search_document
        qs = qs.annotate(
            rank=SearchRank(F("search_document"), search_query),
        )

        # 3) Typo tolerance (trigram)
        qs = qs.annotate(
            similarity=Greatest(
                TrigramSimilarity("title", q),
                TrigramSimilarity("content", q),
            )
        )

        # 4) Combine scores (tune weights to taste)
        qs = qs.annotate(
            score=(F("rank") * 1.0) + (F("similarity") * 0.3)
        )

        # 5) Filter out garbage
        qs = qs.filter(
            Q(rank__gt=0.05) | Q(similarity__gt=0.15)
        ).order_by("-score", "-published")

        return qs
        
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

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

class ListingTagsView(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]

class CRUDTagView(
    GenericViewSet,
    CreateModelMixin, 
    RetrieveModelMixin,
    UpdateModelMixin, 
    DestroyModelMixin,
    ListModelMixin    
):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
