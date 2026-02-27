# Posts/serializers.py

from rest_framework import serializers
from Posts.models import Post, Tag, Category,PostImages
from Comment.serializer import CommentSerializer
from PIL import Image, UnidentifiedImageError

# TODO: both of these serializers is like each other. we can make them one or make them inherits.
class TagsSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag mode.
    """
    class Meta:
        model = Tag
        exclude = ['id']

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Tag mode.
    """
    class Meta:
        model = Category
        exclude = ['id']

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    author_username = serializers.CharField(source='author.username', read_only=True)
    category = CategorySerializer(many = True , read_only = True)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    published_data = serializers.DateTimeField(source='published', read_only=True)

    class Meta:
        model = Post
        # These are the fields that will be converted to JSON
        fields = [
            'title',
            'slug',
            'content',
            'published_data',
            'status',
            'tags',
            'author_username',
            'category',
            # TODO: When I add an image , in API result I see 404 in final link. fix it.
            'cover_image',
            'summary'
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
            'content',
            'slug',
            'published',
            'status',
            'tags',
            'author_username',
            'category',
            'cover_image',
            'comments'
        ]
        read_only_fields = ['author_username']

class BaseImageUploaderSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    MAX_IMAGE_MB = 5242880 # Default is 5 MB, it's in kilobyte format (5 * 1024 * 1024)
    ALLOWED_FORMATS = {"JPEG", "JPG", "PNG", "WEBP"}

    def validate_image(self, file):
        # 1) size check
        if file.size > self.MAX_IMAGE_MB:
            raise serializers.ValidationError(f"Image must be ≤ {self.MAX_IMAGE_MB} MB.")

        # 2) real image check + allowed formats
        # rewind is important because DRF may have already read the file pointer
        pos = file.tell()
        try:
            img = Image.open(file)
            img.verify()  # quick integrity check
        except UnidentifiedImageError:
            raise serializers.ValidationError("Upload must be a valid image.")
        finally:
            file.seek(pos)

        # reopen to read format (some storages require reopen)
        file.seek(0)
        try:
            img = Image.open(file)
            fmt = (img.format or "").upper()
        finally:
            file.seek(0)

        if fmt not in self.ALLOWED_FORMATS:
            allowed = ", ".join(sorted(self.ALLOWED_FORMATS))
            raise serializers.ValidationError(f"Allowed formats: {allowed}.")

        return file

class AvatarUploadSerializer(BaseImageUploaderSerializer):
    MAX_IMAGE_MB = 2097152 # 2 MB
    # ALLOWED_FORMATS same as parent

class CoverImageUploadSerializer(BaseImageUploaderSerializer):
    ...

class PostInilineImageUploadSerializer(BaseImageUploaderSerializer):
    MAX_IMAGE_MB = 8388608 # 8 MB
    # ALLOWED_FORMATS same as parent

class PostsImagesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required = False , allow_null = True)

    class Meta:
        model = PostImages
        fields = '__all__'

    def validate_image(self , file):
        if file is None:
            return None

        validator = PostInilineImageUploadSerializer()
        return validator.validate_image(file)
