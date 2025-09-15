from Authorization.models import CustomAuthenticationUser
from rest_framework import serializers

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
        user = CustomAuthenticationUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        
        return user