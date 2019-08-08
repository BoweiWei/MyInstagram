from django.views.generic import DetailView, TemplateView, ListView
from Insta.models import Post

# Create your views here.
class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    model = Post
    template_name = "index.html"

class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


