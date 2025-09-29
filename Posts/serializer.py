# Posts/serializers.py

from rest_framework import serializers
from Posts.models import Post, Tag, Category
from Comment.serializer import CommentSerializer


class TagsSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag mode.
    """
    class Meta:
        model = Tag
        fields = ['id' , 'name' , 'slug']

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Tag mode.
    """
    class Meta:
        model = Category
        fields = ['id' , 'name' , 'slug']

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    # We can add extra fields or override existing ones here if needed
    # For example, to show the username of the author instead of just the ID.
    author_username = serializers.CharField(source='author.username', read_only=True)
    tags = TagsSerializer(many = True , read_only = True)
    category = CategorySerializer(many = True , read_only = True)

    class Meta:
        model = Post
        # These are the fields that will be converted to JSON
        fields = [
            'id',
            'title',
            'content',
            'slug',
            'published',
            'status',
            'tags',
            'author_username',
            'category',
            # TODO: When I add an image , in API result I see 404 in final link. fix it.
            'cover_image'
        ]
        read_only_fields = ['author_username']

class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for post detail (Post model)
    """
    author_username = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many = True , read_only = True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'published',
            'author_username',
            'comments'
        ]

class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for post detail.
    """
    author_username = serializers.CharField(source = 'author.username' , read_only = True)
    comments = CommentSerializer(many = True, read_only = True)

    class Meta:
        model = Post
        fields = [
            'id',
            'slug',
            'title',
            'image',
            'content',
            'published',
            'author_username',
            'comments'
        ]
