"""
This file contains the views for the Posts app. one of the views is FBV (Function Based View) and the other one is CBV (Class Based View). this isn't have any reason I just wanted to use both of them.
"""

from django.shortcuts import render

from Posts.models import Post
from Comment.forms import CommentForm
from Comment.models import CommentModel

from django.views.generic import DetailView

from django.utils import timezone

def post_list(request):
    # list all the published posts
    all_posts = Post.objects.filter(status='published' , published__lte=timezone.now())
    return render(request, 'post_list.html', {'all_posts': all_posts , 'request' : request.user})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    # Use 'slug_field' and 'slug_url_kwarg' for DetailView to handle slug lookup automatically
    slug_field = 'slug' # The field name on the Post model
    slug_url_kwarg = 'post_slug' # The name of the slug parameter in your URL pattern

    # --- get_context_data ---
    # This is the correct place to add extra context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        context['comments'] = CommentModel.objects.filter(post=post).order_by('-created_at') # Example ordering
        context['comment_form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        # Handle POST request
        if request.method == 'POST':
            form_data = CommentForm(request.POST or None)
            if form_data.is_valid():
                print("form_data" , form_data)
                CommentModel.objects.create(
                    post = self.get_object(),
                    content = form_data.cleaned_data['content'],
                )
                return self.get(request, *args, **kwargs)


"""
Note for creating post function :
if you want to create a post you should use `redirect(new_post.get_absolute_url())` because the `get_absolute_url` method will return the url of the post detail page. (get_absolute_url method is defined in the Post model file.)
"""