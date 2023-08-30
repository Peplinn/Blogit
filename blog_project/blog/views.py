from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
# Create your views here.

posts = [
    {
        'author': 'Ebube',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 7, 2023'
    },
    {
        'author': 'Peter',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 7, 2023'
    }
]

@login_required
def home(request):
    context = {
        #'posts' : Post.objects.all()
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

@login_required
def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
