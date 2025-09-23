from Authorization.models import CustomAuthenticationUser
from rest_framework import serializers
from PIL import Image, UnidentifiedImageError

MAX_AVATAR_MB = 5242880 # 5 MB in kilobyte format (5 * 1024 * 1024)
ALLOWED_FORMATS = {"JPEG", "JPG", "PNG", "WEBP"}

class UsersListingSerializer(serializers.ModelSerializer):
    """
    This serializer using when we want list all users.
    """
    class Meta:
        model = CustomAuthenticationUser
        fields = [
           'id',
           'email',
           'username',
           'is_staff',
           'is_active',
           'last_login',
           'date_joined'
        ]
        read_only_fields = ['id' , 'email' , 'date_joined' , 'last_login' , 'is_staff' , 'is_active']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomAuthenticationUser
        fields = ('username' , 'email' , 'password')
        extra_kwargs = {
            'username' : {'required' : True},
            'email' : {'required' : True},
        }

    def create(self , validated_data):
        user = CustomAuthenticationUser.objects.create_user(**validated_data)
        return user

class AvatarUploadSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=True)

    def validate_avatar(self, file):
        # 1) size check
        if file.size > MAX_AVATAR_MB:
            raise serializers.ValidationError(f"Avatar must be ≤ {MAX_AVATAR_MB} MB.")

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

        if fmt not in ALLOWED_FORMATS:
            allowed = ", ".join(sorted(ALLOWED_FORMATS))
            raise serializers.ValidationError(f"Allowed formats: {allowed}.")

        return file

