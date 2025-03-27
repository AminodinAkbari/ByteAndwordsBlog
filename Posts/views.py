"""
This file contains the views for the Posts app. one of the views is FBV (Function Based View) and the other one is CBV (Class Based View). this isn't have any reason I just wanted to use both of them.
"""

from django.shortcuts import render

from Posts.models import Post
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

def post_list(request):
    # list all the posts
    all_posts = Post.objects.all()
    
    return render(request, 'post_list.html', {'all_posts': all_posts})

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        # get the post by slug
        slug = self.kwargs.get('post_slug')
        return get_object_or_404(Post, slug=slug)


"""
Note for creating post function :
if you want to create a post you should use `redirect(new_post.get_absolute_url())` because the `get_absolute_url` method will return the url of the post detail page. (get_absolute_url method is defined in the Post model file.)
"""