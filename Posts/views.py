from django.shortcuts import render
from Posts.models import Post

def post_list(request):
    # list all the posts
    all_posts = Post.objects.all()
    
    return render(request, 'post_list.html', {'all_posts': all_posts})

def detail_view(request, post_slug):
    # get the post with the given id
    post = Post.objects.get(slug=post_slug)
    
    return render(request, 'blog_detail.html', {'post': post})


"""
Note for creating post function :
if you want to create a post you should use `redirect(new_post.get_absolute_url())` because the `get_absolute_url` method will return the url of the post detail page. (get_absolute_url method is defined in the Post model file.)
"""