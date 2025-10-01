from rest_framework.generics import RetrieveUpdateAPIView
from User.serializer import UsersListingSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from Authorization.models import CustomAuthenticationUser

# TODO: We have Authorization and User model. check we correct about it ? we should remove one of those ?

class CurrentUserAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersListingSerializer

    def get_object(self):
        return self.request.user
