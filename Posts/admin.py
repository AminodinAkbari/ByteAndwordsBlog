from django.contrib import admin
from Posts.models import Post,Tag,Category

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)