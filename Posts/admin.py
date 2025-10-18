from django.contrib import admin
from Posts.models import Post,Tag,Category,PostImages

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(PostImages)
