import django_filters
from Posts.models import Post

class TagFilter(django_filters.FilterSet):
    """
    FilterSet for filtering Posts by tags.

    This filter set allows for filtering Posts by tags. The tag filter
    is case-insensitive and allows for filtering by slug.

    The available filters are:

    - tag: a case-insensitive filter for filtering by tag slug.

    For example, /posts/?tag=python would return all Posts that have a
    tag with slug "python".

    """
    # Allow ?tag=<slug>, case-insensitive
    tag = django_filters.CharFilter(field_name='tags__slug', lookup_expr='iexact')

    class Meta:
        model = Post
        fields = ['tag']
