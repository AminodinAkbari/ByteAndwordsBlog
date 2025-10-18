"""
URL configuration for Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from Posts.views import PostViewSet,PostsImagesView
from Authorization.views import CurrentUserAPI
from User.views import meViewSet

from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', PostViewSet.as_view({"get" : "list"}) , name = 'posts-list'),
    path('posts/<slug:slug>/', PostViewSet.as_view({"get" : "retrieve"}) , name = 'post-detail'),
    path('posts/by-tag/<tag>/' , PostViewSet.as_view({"get" : "retrieve_posts_by_tag"}) , name = 'post-by-tag'),
    
    path('post_images/', PostsImagesView.as_view({"get": "list", "post": "create"})),
    
    path('post_images/<pk>/', PostsImagesView.as_view({
        "get": "retrieve", 
        "delete": "destroy", 
        "put": "update",
        "patch": "partial_update"
    })),
    
    path('me/', CurrentUserAPI.as_view(), name='current-user'),

    # Button for login/logout pages for the DRF browsable API only.
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

# Include tokens
urlpatterns += [
    path('token/' , TokenObtainPairView.as_view() , name="token_obtain"),
    path('token/refresh' , TokenRefreshView.as_view() , name="token_refresh")
]

# Including all current user urls
me_avatar = meViewSet.as_view({"patch" : "avatar"})
me_view_urls = [
    path('me/avatar/' , me_avatar , name = "current_user_change_avatar")
]
urlpatterns += me_view_urls

