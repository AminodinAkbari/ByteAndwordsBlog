from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


from Authorization.models import CustomAuthenticationUser
from User.serializer import AvatarUploadSerializer

class meViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AvatarUploadSerializer

    @action(detail = False,methods = ["patch"],url_path = "avatar")
    def avatar(self , request):

        serializer = AvatarUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        user = request.user

        # Get old avatar if exists and remove it from server storage
        old_avatar = user.avatar.name if user.avatar else None

        user.avatar = serializer.validated_data["image"]
        user.save(update_fields = ["avatar"])

        if old_avatar and old_avatar != user.avatar.name:
            user._meta.get_field("avatar").storage.delete(old_avatar)

        return Response({"avatar_url" : user.avatar.url if user.avatar else None} , status =status.HTTP_200_OK )
