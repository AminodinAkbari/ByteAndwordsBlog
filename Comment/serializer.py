# Comment/serializers.py
from rest_framework import serializers
from Comment.models import CommentModel

class CommentSerializer(serializers.ModelSerializer):
    # Display the author's username instead of their ID
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = CommentModel
        fields = [
            'id',
            'content',
            'author',
            'author_username',
            'created_at',
            'post', # We need the post ID to know which post it belongs to
        ]
        # The author and post will be set automatically in the view, not by the user sending the data.
        read_only_fields = ['author', 'post']