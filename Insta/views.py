from annoying.decorators import ajax_request
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin

from Insta.forms import CustomUserCreationForm
from Insta.models import Post, Like, Comment

# Create your views here.
class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    model = Post
    template_name = "index.html"

# Use the models Post on to the post_detail html file
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

# Controller for creating post
# LoginRequiredMixin is identifier to see whether user is logged in.
# otherwise createview is not perimitted
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    # let user to provide all the info in model called Post
    fields = '__all__'
    # if not login yet, sys will direct user to the login html
    # after login, it will redirect back to PostCreateView again
    login_url = 'login'
    

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    # only title is allowed to update at this point
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    # if delete while jump, use reverse_lazy instead of reverse
    # success_url is the page you gonna jump to if the process is succeed
    success_url = reverse_lazy('posts')

class SignUp(CreateView):
    # form_class is the instruction to create this user
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('posts')

# @ajax_request means this function only response to ajax, so no need to 
# render it to a html file
@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        # save the like into the database
        like.save()
        result = 1
    except Exception as e:
        # if the like already exist, delete this action
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0
    # return json with result
    return {
        'result': result,
        'post_pk': post_pk
    }


@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }