from typing import Optional
from django.forms.models import BaseModelForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # Find the rest
from .models import Tale
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
    # context = {
    #     #'posts' : Post.objects.all()
    #     'tales' : Tale.objects.all()
    # }
    context = {
        'latest_tale' : Tale.objects.latest('date_posted')
    }

    return render(request, 'blog/home.html', context)

class TaleListView(ListView):
    # Don't forget to implement pagination
    model = Tale
    template_name = 'blog/tales.html' # Expected format: <app>/<model>_<viewtype>.html
    context_object_name = 'tales'
    ordering = ['-number']

    paginate_by = 3
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tales'  # Add the page title to the context
        return context
    # paginate_by = 5

class TaleDetailView(DetailView):
    model = Tale
    template_name = 'blog/tale_detail.html' # Expected format: <app>/<model>_<viewtype>.html
    context_object_name = 'tale'

    def get_object(self):
        number = self.kwargs.get('number')  # Get the 'number' from the URL
        return get_object_or_404(Tale, number=number)

# @method_decorator(login_required, name = 'dispatch') #Functional, but we will replace this with a mixin
# class TaleListView(LoginRequiredMixin, ListView):
#     model = Tale
#     template_name = 'blog/home.html' # Expected format: <app>/<model>_<viewtype>.html
#     context_object_name = 't
# ales'
#     ordering = ['-date_posted']
#     paginate_by = 5

class UserTaleListView(ListView):
    model = Tale
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tales'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Tale.objects.filter(author=user).order_by('-date_posted')

# class TaleDetailView(DetailView):
#     model = Tale

class TaleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tale
    success_url = '/'

    def test_func(self):
        tale = self.get_object()
        if self.request.user == tale.author:
            return True
        return False

# @method_decorator(login_required, name = 'dispatch')
class TaleCreateView(LoginRequiredMixin, CreateView):
    model = Tale
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tale
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        tale = self.get_object()
        if self.request.user == tale.author:
            return True
        return False

# @login_required
def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

# @login_required
def tales(request):
    return render(request, 'blog/tales.html', {'title':'Tales'})
