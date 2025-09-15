from rest_framework.views import APIView
from User.serializer import UsersListingSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import permissions, status

from Authorization.models import CustomAuthenticationUser

# TODO: We have Authorization and User model. check we correct about it ? we should remove one of those ?

class UserAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return [permission() for permission in self.permission_classes]

    def get(self , request):
        users = CustomAuthenticationUser.objects.all()
        print(users)
        _serializer_ = UsersListingSerializer(users , many=True)
        return Response(_serializer_.data)

    def post(self , request):
        # TODO: add permission for this API.
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_registration = serializer.save()

            return Response(UserRegistrationSerializer(user_registration).data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
