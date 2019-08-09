from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin

from Insta.forms import CustomUserCreationForm
from Insta.models import Post

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

