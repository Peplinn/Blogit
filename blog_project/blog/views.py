from typing import Optional
from django.forms.models import BaseModelForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.http import HttpResponse
# Create your views here.

# posts = [
#     {
#         'author': 'Ebube',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 7, 2023'
#     },
#     {
#         'author': 'Peter',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 7, 2023'
#     }
# ]

# @login_required
def home(request):
    context = {
        #'posts' : Post.objects.all()
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# @method_decorator(login_required, name = 'dispatch') #Functional, but we will replace this with a mixin
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html' # Expected format: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# @method_decorator(login_required, name = 'dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# @login_required
def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

# @login_required
def tales(request):
    return render(request, 'blog/tales.html', {'title':'Tales'})
