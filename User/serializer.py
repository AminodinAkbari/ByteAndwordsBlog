from Authorization.models import CustomAuthenticationUser
from rest_framework import serializers
from PIL import Image, UnidentifiedImageError

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

<<<<<<< HEAD
=======
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
>>>>>>> 02ee2a8adf0ba8c02bfc474c513cfc5256144fda
