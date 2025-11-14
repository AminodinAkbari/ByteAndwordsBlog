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
