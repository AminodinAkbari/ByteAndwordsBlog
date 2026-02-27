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
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.urls import path, include
from Posts.views import (
    PublishedPostViewSet,
    CRUDPostsViewset,
    PostsImagesView,
    PostsByTagView,
    CRUDTagView,
    SearchPostsView
    )
from Authorization.views import CurrentUserAPI
from User.views import meViewSet
from Utils.Health.test_db_connection import health_check

from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

router = DefaultRouter(trailing_slash=False) 
router.register(r'posts-lists' , PublishedPostViewSet, basename = 'posts')
router.register(r'post' , CRUDPostsViewset, basename = 'post')
router.register(r'posts-by-tag' , PostsByTagView, basename = 'posts-by-tag')
router.register(r'posts' , SearchPostsView , basename = 'posts-search')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post_images/', PostsImagesView.as_view({"get": "list", "post": "create"})),
    path('post_images/<pk>/', PostsImagesView.as_view({
        "get": "retrieve",
        "delete": "destroy",
        "put": "update",
        "patch": "partial_update"
    })),

    path('tags/', CRUDTagView.as_view({"get" : "list"})),
    path('tags/<slug>', CRUDTagView.as_view({
        "post" : "create",
        "get": "retrieve",
        "delete": "destroy",
        "patch": "partial_update"
    })),

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

# Healt endpoints
health_endpoints = [
    path('db_health' , health_check , name = "database_health_check")
]

urlpatterns += me_view_urls
urlpatterns += router.urls
urlpatterns += health_endpoints
